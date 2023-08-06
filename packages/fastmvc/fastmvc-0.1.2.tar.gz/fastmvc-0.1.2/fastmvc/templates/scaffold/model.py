from fastmvc.models.database.^{platform.data_model_import}^


class ^{Obj}^(^{platform.data_model}^):
    ^{model_attrs}^

    class Config:
        table_name = "^{proj}^_^{obj}^"