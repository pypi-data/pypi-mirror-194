from typing import Dict
from typing import Set

from idem_gcp.tool.gcp.schema.results_collector import ResultsCollector


def check(
    hub, current_schema: Dict, essential_resources: Set[str] = None
) -> ResultsCollector:
    collector = ResultsCollector()

    for method in current_schema.keys():
        method_path = f"root['{method}']"
        if not hub.tool.gcp.case.is_snake_case(method):
            collector.add_breaking(
                schema_path=method_path, description="method name is not in snake_case"
            )
        parameters: Dict = current_schema.get(method).get("parameters") or {}
        for parameter in parameters.keys():
            if not hub.tool.gcp.case.is_snake_case(parameter):
                parameter_path = f"{method_path}['parameters']['{parameter}']"
                collector.add_breaking(
                    schema_path=parameter_path,
                    description="parameter name is not in snake_case",
                )

    return collector
