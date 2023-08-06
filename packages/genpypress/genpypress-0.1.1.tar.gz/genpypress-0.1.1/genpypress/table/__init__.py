from attrs import define, field


class Rules:
    keys: list[str] = field(default=list())
    map: dict[str, str] = field(default=dict())


class Column:
    name: str = field(default="")
    comment: str = field(default="")
    data_type: str = field(default="")
    data_type_base: str = field(default="")
    scale: int = field(default=0)
    precission: int = field(default=0)
    is_derived: bool = field(default=False)
    is_derived_from: str = field(default="")
    is_derived_to: str = field(default="")
    is_validtime: bool = field(default=False)
    is_transactiontime: bool = field(default=False)
    compress: str = field(default="")
    character_set: str = field(default="")
    case_specific: bool = field(default=False)
    primary: bool = field(default=False)
    etl_src_not_available: bool = field(default=False)
    etl_crc_format: str = field(default="")
    etl_src_header: str = field(default="")
    etl_src_size_in_bytes: int = field(default=0)
    rules: Rules = field(default=Rules())
    cdc_src_column: str = field(default="")
    cdc_src_data_type: str = field(default="")
    cdc_src_scale: int = field(default=0)


class Table:
    database: str = field(default="")
    name: str = field(default="")
    comment: str = field(default="")
    set_or_multiset: str = field(default="")
    pi_is_upi: bool = field(default=False)
    pi_name: str = field(default="")