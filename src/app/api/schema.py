from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework.request import Request

tags_for_customization = [
    "categories",
    "companies",
    "departments",
    "employees",
    "master-procedure",
    "material-types",
    "materials",
    "points",
    "procedure",
    "products",
    "stocks",
]


def _customize_parameters(parameters: dict, tags: list[str]) -> None:
    if all(tag not in tags_for_customization for tag in tags):
        return
    for parameter in parameters:
        new_parameter = OpenApiParameter(parameter["name"], OpenApiTypes.INT, OpenApiParameter.PATH)
        parameter["in"] = str(new_parameter.location)
        parameter["schema"]["type"] = str(new_parameter.type)
        parameter["required"] = True


def postprocessing_hook(result: dict, generator: SchemaGenerator, request: Request, public: bool) -> dict:
    for methods in result["paths"].values():
        for data in methods.values():
            parameters = data.get("parameters")
            tags = data.get("tags")
            if not parameters or not tags:
                continue
            _customize_parameters(parameters, tags)
    return result
