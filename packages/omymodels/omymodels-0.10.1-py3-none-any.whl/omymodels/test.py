from omymodels import convert_models, create_models

ddl = """
CREATE TABLE "schema--notification"."notification" (
    content_type "schema--notification"."ContentType",
    period "schema--notification"."Period"
);
"""
result = create_models(ddl)
#result = convert_models(models_from, models_type="gino")
print(result['metadata'])
