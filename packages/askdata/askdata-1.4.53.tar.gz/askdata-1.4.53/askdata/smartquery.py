import json
import os
import re
from enum import Enum, auto
from typing import List, Optional, Union, Dict
from dataclasses import dataclass

consistent_datatypes = {"numeric": ["bit", "smallmoney", "money", "int",
                                    "decimal", "decimal(4,2)", "decimal(3,2)", "float", "float64", "double",
                                    "bigdecimal", "int32", "int64", "bigint",
                                    "numeric", "bignumeric", "smallint", "integer",
                                    "tinyint", "byteint", "int8", "long",
                                    "float8", "hugeint", "int4", "signed",
                                    "real", "float4", "int2", "short",
                                    "int1", "ubigint", "uinteger", "usmallint",
                                    "utinyint", "bool", "boolean", "mediumint",
                                    "double precision", "dec", "smallserial", "serial",
                                    "bigserial", "number", "number(3,2)", "binary", "smalldecimal"],
                        "date":
                            ["date", "datetimeoffset", "datetime2", "smalldatetime",
                             "timestamp", "datetime", "time", "year",
                             "interval", "timestamp_ltz", "timestamp_ntz", "timestamp_tz", "text"],
                        "string":
                            ["string", "varchar", "varchar2", "char",
                             "bpchar", "text", "nchar", "nvarchar",
                             "tinyblob", "blob", "shorttext", "clob",
                             "nclob", "ntext", "tinytext", "mediumtext",
                             "longtext", "mediumblob", "longblob", "image",
                             "character", "character varying", "binary", "varbinary"]}


def change_operator(operator):
    if operator == "GOE":
        operator = ">="
    elif operator == "LOE":
        operator = "<="
    elif operator == "EQ":
        operator = "=="
    elif operator == "GT":
        operator = ">"
    elif operator == "LT":
        operator = "<"
    return operator


class SQLFunction(Enum):
    MAX = auto()
    MIN = auto()
    AVG = auto()
    COUNT = auto()
    SUM = auto()


class TimeDimensionGranularity(Enum):
    year = auto()
    quarter = auto()
    month = auto()
    week = auto()
    day = auto()
    hour = auto()
    interval = auto()


class SignOperator(Enum):
    NEXT = auto()
    PREV = auto()


@dataclass
class Field:
    column: Optional[str] = None
    aggregation: Optional[Union[SQLFunction, TimeDimensionGranularity, str]] = None
    dataset: Optional[str] = None
    entityType: Optional[str] = None
    alias: Optional[str] = None
    complexExpression: Optional[str] = None
    internalDataType: Optional[str] = None
    sourceDataType: Optional[str] = None
    sqlExpression: Optional[str] = None
    sourceFormat: Optional[str] = None

    def __repr__(self):
        if self.column is not None:
            if self.aggregation is not None:
                if isinstance(self.aggregation, SQLFunction) or isinstance(self.aggregation,
                                                                            TimeDimensionGranularity):
                    field_with_agg = self.aggregation.name + " ( " + self.column + " )"
                else:
                    field_with_agg = self.aggregation + " ( " + self.column + " )"
            else:
                field_with_agg = self.column
        elif self.complexExpression is not None:
            field_with_agg = self.complexExpression
        if self.alias is not None:
            field_with_agg += " AS " + self.alias
        return field_with_agg


class SQLOperator(Enum):
    EQ = auto()
    NOT_EQ = auto()
    GOE = auto()
    GT = auto()
    LOE = auto()
    LT = auto()
    IN = auto()
    NOT_IN = auto()
    SEARCH = auto()
    TIMESPAN = auto()
    FOREACH = auto()


class PatternOperator(Enum):
    START = auto()
    END = auto()
    CONTAINS = auto()


class BooleanOperator(Enum):
    AND = auto()
    OR = auto()


class PeriodOperator(Enum):
    PREV = auto()
    CURR = auto()
    NEXT = auto()


class TimeOperator(Enum):
    RANGE = auto()
    FROM = auto()
    TO = auto()


@dataclass
class Condition:
    field: Field
    operator: Optional[Union[SQLOperator, TimeOperator, PatternOperator, str]] = None
    value: Optional[List[Union[float, str]]] = None
    conditionValues: Optional[List[Dict]] = None
    type: Optional[str] = None
    steps: Optional[str] = None
    interval: Optional[str] = None
    direction: Optional[Union[PeriodOperator, str]] = None
    negate: Optional[bool] = None

    def __repr__(self):
        vars = []
        if self.negate is not None:
            negation = "NOT"
        else:
            negation = None
        if self.value is not None:
            for var in self.value:
                vars.append(str(var))
            formatted_value = "( " + ", ".join(vars) + " )"
        else:
            formatted_value = None

        if isinstance(self.operator, str):
            operator = self.operator
        elif isinstance(self.operator, SQLOperator) or isinstance(self.operator, TimeOperator):
            operator = self.operator.name
            operator = change_operator(operator)
        else:
            operator = None
        if self.field.column is not None:
            field_with_agg = self.field.column
            if self.field.aggregation is not None:
                if isinstance(self.field.aggregation, SQLFunction) or isinstance(self.field.aggregation,
                                                                                 TimeDimensionGranularity):
                    field_with_agg = self.field.aggregation.name + " ( " + field_with_agg + " )"
                else:
                    field_with_agg = self.field.aggregation + " ( " + field_with_agg + " )"
        elif self.field.complexExpression is not None:
            field_with_agg = self.field.complexExpression

        if self.field.complexExpression is None:
            if self.direction is None:
                if negation is None:
                    where_condition = (
                            field_with_agg + " " + operator + " " + str(formatted_value)
                    )
                else:
                    where_condition = (
                        field_with_agg + " " + negation + " " + operator + " " + str(formatted_value)
                    )
            elif self.direction is not None:
                if isinstance(self.direction, PeriodOperator):
                    direction = self.direction.name
                else:
                    direction = self.direction
                if negation is None:
                    if self.steps is not None and self.interval is not None:
                        where_condition = (
                                field_with_agg + " " + operator + " " + self.interval + " " + direction + " " + self.steps
                        )
                    elif self.steps is not None and self.interval is None:
                        where_condition = (
                                field_with_agg + " " + operator + " " + direction + " " + self.steps
                        )
                    elif self.steps is None and self.interval is not None:
                        where_condition = (
                                field_with_agg + " " + operator + " " + self.interval + " " + direction
                        )
                    else:
                        where_condition = (
                                field_with_agg + " " + operator + " " + direction
                        )
                else:
                    if self.steps is not None and self.interval is not None:
                        where_condition = (
                                field_with_agg + " " + negation + " " + operator + " " + self.interval + " " + direction + " " + self.steps
                        )
                    elif self.steps is not None and self.interval is None:
                        where_condition = (
                                field_with_agg + " " + negation + " " + operator + " " + direction + " " + self.steps
                        )
                    elif self.steps is None and self.interval is not None:
                        where_condition = (
                                field_with_agg + " " + negation + " " + operator + " " + self.interval + " " + direction
                        )
                    else:
                        where_condition = (
                                field_with_agg + " " + negation + " " + operator + " " + direction
                        )
            elif operator is not None:
                if negation is None:
                    where_condition = (
                            field_with_agg + " " + operator
                    )
                else:
                    where_condition = (
                        field_with_agg + " " + negation + " " + operator
                    )
            else:
                where_condition = (
                    field_with_agg
                )
        else:
            where_condition = (
                field_with_agg
            )

        return where_condition


@dataclass
class CompositeCondition:
    operator: Union[BooleanOperator, str]
    conditions: List[Union[Condition, 'CompositeCondition']]

    def __repr__(self):
        if isinstance(self.operator, BooleanOperator):
            where_condition = '( ' + (' ' + self.operator.name + ' ').join([str(c) for c in self.conditions]) + ' )'
        else:
            where_condition = '( ' + (' ' + self.operator + ' ').join([str(c) for c in self.conditions]) + ' )'

        return where_condition


class SQLSorting(Enum):
    DESC = auto()
    ASC = auto()


@dataclass
class Sorting:
    field: str
    order: Union[SQLSorting, str]

    def __repr__(self):
        if isinstance(self.order, SQLSorting):
            return self.field + " " + self.order.name
        return self.field + " " + self.order


@dataclass
class Component:
    type: str
    queryId: str


@dataclass
class QueryComponent(Component):
    category: str


@dataclass
class ChartComponent(Component):
    chartType: str


@dataclass
class MapComponent(Component):
    mapType: str


@dataclass
class From:
    dataset: str


@dataclass
class Join:
    query: str
    workspace: Optional[str] = None
    dataset: Optional[str] = None
    on: Optional[List[str]] = None
    left_on: Optional[List[str]] = None
    right_on: Optional[List[str]] = None


@dataclass
class GroupBy:
    field: Field


@dataclass
class UnmatchedField:
    value: str
    confidence: str
    type: Optional[str] = None


@dataclass
class Query:
    fields: List[Union[Field]]
    pivot: Optional[List[Field]] = None
    join: Optional[List[Join]] = None
    id: Optional[str] = None
    datasets: Optional[List[From]] = None
    where: Optional[List[Union[Condition, CompositeCondition]]] = None
    groupBy: Optional[List[GroupBy]] = None
    orderBy: Optional[List[Sorting]] = None
    limit: Optional[Union[int, str]] = None
    offset: Optional[Union[int, str]] = None
    unmatched: Optional[List[UnmatchedField]] = None

    def to_sql(self, dataset: str = None):
        sql = "SELECT {} FROM {}"

        fields_with_agg = [str(field) for field in self.fields]
        formatted_fields = ", ".join(fields_with_agg)

        if self.datasets is not None and self.datasets:
            froms_array = [d.dataset for d in self.datasets]
            table = ", ".join(froms_array)
        elif dataset is not None:
            table = dataset
        else:
            table = "{{dataset.A}}"
        sql = sql.format(formatted_fields, table)

        if self.where is not None:
            sql_where = " WHERE {}"

            where_conditions = [str(condition) for condition in self.where]
            if where_conditions:
                formatted_where_conditions = " AND ".join(where_conditions)
                sql_where = sql_where.format(formatted_where_conditions)
                sql += sql_where

        if self.orderBy is not None:
            sql_orderby = " ORDER BY {}"
            sorting_conditions = [str(sorting) for sorting in self.orderBy]
            formatted_sorting = ", ".join(sorting_conditions)
            sql_orderby = sql_orderby.format(formatted_sorting)
            sql += sql_orderby

        if self.limit is not None:
            sql += " LIMIT " + str(self.limit)

        return sql

    def _field_spell_out(self, field):
        # otherwise, check if internal and original data types are not consistent each other
        global consistent_datatypes
        consistent_vec = consistent_datatypes[field.internalDataType.lower()]
        if (
                field.internalDataType.lower() == "numeric" or field.internalDataType.lower() == "string") and field.sourceDataType.lower() not in consistent_vec:
            # if internal and original data types are not consistent each other use this pattern
            # aggregation column (original data type, to internal data type ) AS Alias
            if field.alias is None:
                if field.aggregation is not None and isinstance(field.aggregation, str):
                    string = '"' + field.aggregation + " " + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ")" + '"'
                elif field.aggregation is not None and isinstance(field.aggregation, SQLFunction):
                    string = '"' + field.aggregation.name + " " + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ")" + '"'
                else:
                    string = '"' + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ")" + '"'
            else:
                if field.aggregation is not None and isinstance(field.aggregation, str):
                    string = '"' + field.aggregation + " " + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ") AS " + field.alias + '"'
                elif field.aggregation is not None and isinstance(field.aggregation, SQLFunction):
                    string = '"' + field.aggregation.name + " " + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ") AS " + field.alias + '"'
                else:
                    string = '"' + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ") AS " + field.alias + '"'
        elif field.internalDataType.lower() == "date" and field.sourceDataType.lower() not in consistent_vec:
            # if internal and original data types are not consistent each other use this pattern
            # aggregation column (original data type, to internal data type, date_format YYYY-MM-DD ) AS Alias
            if field.sourceFormat is not None:
                if field.alias is None:
                    if field.aggregation is not None and isinstance(field.aggregation, str):
                        string = '"' + field.aggregation + " " + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ", format " + field.sourceFormat + ")" + '"'
                    elif field.aggregation is not None and isinstance(field.aggregation, SQLFunction):
                        string = '"' + field.aggregation.name + " " + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ", format " + field.sourceFormat + ")" + '"'
                    else:
                        string = '"' + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ", format " + field.sourceFormat + ")" + '"'
                else:
                    if field.aggregation is not None and isinstance(field.aggregation, str):
                        string = '"' + field.aggregation + " " + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ", format " + field.sourceFormat + ") AS " + field.alias + '"'
                    elif field.aggregation is not None and isinstance(field.aggregation, SQLFunction):
                        string = '"' + field.aggregation.name + " " + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ", format " + field.sourceFormat + ") AS " + field.alias + '"'
                    else:
                        string = '"' + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ", format " + field.sourceFormat + ") AS " + field.alias + '"'
            else:
                if field.alias is None:
                    if field.aggregation is not None and isinstance(field.aggregation, str):
                        string = '"' + field.aggregation + " " + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ", format YYYY-MM-DD" + ")" + '"'
                    elif field.aggregation is not None and isinstance(field.aggregation, SQLFunction):
                        string = '"' + field.aggregation.name + " " + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ", format YYYY-MM-DD" + ")" + '"'
                    else:
                        string = '"' + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ", format YYYY-MM-DD" + ")" + '"'
                else:
                    if field.aggregation is not None and isinstance(field.aggregation, str):
                        string = '"' + field.aggregation + " " + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ", format YYYY-MM-DD" + ") AS " + field.alias + '"'
                    elif field.aggregation is not None and isinstance(field.aggregation, SQLFunction):
                        string = '"' + field.aggregation.name + " " + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ", format YYYY-MM-DD" + ") AS " + field.alias + '"'
                    else:
                        string = '"' + field.column + " (" + field.sourceDataType + ", to " + field.internalDataType + ", format YYYY-MM-DD" + ") AS " + field.alias + '"'
        else:
            # else
            if field.alias is None:
                if field.aggregation is not None and isinstance(field.aggregation, str):
                    string = '"' + field.aggregation + " " + field.column + " (" + field.sourceDataType + ")" + '"'
                elif field.aggregation is not None and isinstance(field.aggregation, SQLFunction):
                    string = '"' + field.aggregation.name + " " + field.column + " (" + field.sourceDataType + ")" + '"'
                else:
                    string = '"' + field.column + " (" + field.sourceDataType + ")" + '"'
            else:
                if field.aggregation is not None and isinstance(field.aggregation, str):
                    string = '"' + field.aggregation + " " + field.column + " (" + field.sourceDataType + ") AS " + field.alias + '"'
                elif field.aggregation is not None and isinstance(field.aggregation, SQLFunction):
                    string = '"' + field.aggregation.name + " " + field.column + " (" + field.sourceDataType + ") AS " + field.alias + '"'
                else:
                    string = '"' + field.column + " (" + field.sourceDataType + ") AS " + field.alias + '"'
        return string

    def _where_spell_out(self, where):
        global consistent_datatypes
        conditions = []

        for where_condition in where:
            if isinstance(where_condition, Condition):
                if where_condition.field.column is not None:
                    vars = []

                    if where_condition.value is not None:
                        for var in where_condition.value:
                            vars.append(str(var))
                        formatted_value = "( " + ", ".join(vars) + " )"
                    else:
                        formatted_value = None

                    if isinstance(where_condition.operator, str):
                        if where_condition.negate is None:
                            operator = where_condition.operator
                        else:
                            operator = "NOT " + where_condition.operator
                    elif isinstance(where_condition.operator, SQLOperator) or isinstance(where_condition.operator,
                                                                                         TimeOperator):
                        operator = where_condition.operator.name
                        if operator == "IN":
                            if where_condition.negate is None:
                                operator = where_condition.operator.name
                            else:
                                operator = "NOT " + where_condition.operator.name
                        elif operator == "GOE":
                            if where_condition.negate is None:
                                operator = ">="
                            else:
                                operator = "<"
                        elif operator == "LOE":
                            if where_condition.negate is None:
                                operator = "<="
                            else:
                                operator = ">"
                        elif operator == "EQ":
                            if where_condition.negate is None:
                                operator = "=="
                            else:
                                operator = "!="
                        elif operator == "GT":
                            if where_condition.negate is None:
                                operator = ">"
                            else:
                                operator = "<="
                        elif operator == "LT":
                            if where_condition.negate is None:
                                operator = "<"
                            else:
                                operator = ">="
                    else:
                        operator = None

                    field_with_agg = where_condition.field.column
                    if where_condition.field.aggregation is not None:
                        if isinstance(where_condition.field.aggregation, SQLFunction) or isinstance(where_condition.field.aggregation,
                                                                                         TimeDimensionGranularity):
                            field_with_agg = where_condition.field.aggregation.name + " ( " + field_with_agg + " )"
                        else:
                            field_with_agg = where_condition.field.aggregation + " ( " + field_with_agg + " )"

                    if where_condition.field.internalDataType is not None:
                        consistent_vec = consistent_datatypes[where_condition.field.internalDataType.lower()]
                        if (
                                where_condition.field.internalDataType.lower() == "numeric" or where_condition.field.internalDataType.lower() == "string") \
                                and where_condition.field.sourceDataType.lower() in consistent_vec:
                            # if internal and original data types are not consistent each other use this pattern
                            # aggregation column (original data type, to internal data type ) AS Alias
                            formatted_cond = field_with_agg + " (" + where_condition.field.sourceDataType + ", to " + where_condition.field.internalDataType + ") " + operator + " " + formatted_value
                        elif where_condition.field.internalDataType.lower() == "date" and where_condition.field.sourceDataType.lower() in consistent_vec:
                            # if internal and original data types are not consistent each other use this pattern
                            # aggregation column (original data type, to internal data type, date_format YYYY-MM-DD ) AS Alias
                            if where_condition.field.sourceFormat is not None:
                                formatted_cond = field_with_agg + " (" + where_condition.field.sourceDataType + \
                                                 ", to " + where_condition.field.internalDataType + ", format " + \
                                                 where_condition.field.sourceFormat + ") " + operator + " " + \
                                                 formatted_value
                            else:
                                if where_condition.direction is None:
                                    formatted_cond = field_with_agg + " (" + where_condition.field.sourceDataType + \
                                                     ", to " + where_condition.field.internalDataType + ") " + \
                                                     operator + " " + formatted_value
                                else:
                                    if isinstance(where_condition.direction, PeriodOperator):
                                        direction = where_condition.direction.name
                                    else:
                                        direction = where_condition.direction

                                    if where_condition.steps is not None:
                                        formatted_cond = field_with_agg + " (" + where_condition.field.sourceDataType + \
                                                         ", to " + where_condition.field.internalDataType + ") " + \
                                                         operator + " " + direction + " " + where_condition.steps + \
                                                         " " + formatted_value
                                    else:
                                        formatted_cond = field_with_agg + " (" + where_condition.field.sourceDataType + \
                                                         ", to " + where_condition.field.internalDataType + ") " + \
                                                         operator + " " + direction + " " + formatted_value
                        elif where_condition.field.complexExpression is not None:
                            if where_condition.field.alias is not None:
                                formatted_cond = where_condition.field.complexExpression + " AS " + where_condition.field.alias
                            else:
                                formatted_cond = where_condition.field.complexExpression

                        conditions.append(formatted_cond)
                elif where_condition.field.complexExpression is not None:
                    formatted_cond = where_condition.field.complexExpression
                    conditions.append(formatted_cond)
            elif isinstance(where_condition, CompositeCondition):
                other_conds = self._where_spell_out(where_condition.conditions)
                if where_condition.operator.name == "AND":
                    conditions = other_conds
                elif where_condition.operator.name == "OR":
                    conditions.append(" OR ".join(other_conds))
        return conditions

    def spell_out(self, add_offset=True):
        spell_str = '{"fields":['

        fields = []
        for field in self.fields:
            # if there is sql expression it always wins
            if field.sqlExpression is not None:
                if field.alias is None:
                    if field.aggregation is not None and isinstance(field.aggregation, str):
                        string = '"' + field.aggregation + " " + field.sqlExpression + '"'
                    elif field.aggregation is not None and isinstance(field.aggregation, SQLFunction):
                        string = '"' + field.aggregation.name + " " + field.sqlExpression + '"'
                    else:
                        string = '"' + field.sqlExpression + '"'
                else:
                    if field.aggregation is not None and isinstance(field.aggregation, str):
                        string = '"' + field.aggregation + " " + field.sqlExpression + " AS " + field.alias + '"'
                    elif field.aggregation is not None and isinstance(field.aggregation, SQLFunction):
                        string = '"' + field.aggregation.name + " " + field.sqlExpression + " AS " + field.alias + '"'
                    else:
                        string = '"' + field.sqlExpression + " AS " + field.alias + '"'
            elif field.complexExpression is not None:
                if field.alias is None:
                    if field.aggregation is not None and isinstance(field.aggregation, str):
                        string = '"' + field.aggregation + " " + field.complexExpression + '"'
                    elif field.aggregation is not None and isinstance(field.aggregation, SQLFunction):
                        string = '"' + field.aggregation.name + " " + field.complexExpression + '"'
                    else:
                        string = '"' + field.complexExpression + '"'
                else:
                    if field.aggregation is not None and isinstance(field.aggregation, str):
                        string = '"' + field.aggregation + " " + field.complexExpression + " AS " + field.alias + '"'
                    elif field.aggregation is not None and isinstance(field.aggregation, SQLFunction):
                        string = '"' + field.aggregation.name + " " + field.complexExpression + " AS " + field.alias + '"'
                    else:
                        string = '"' + field.complexExpression + " AS " + field.alias + '"'
            elif field.internalDataType is not None:
                string = self._field_spell_out(field)
            else:
                if field.alias is None:
                    if field.aggregation is not None and isinstance(field.aggregation, str):
                        string = '"' + field.aggregation + " " + field.column + '"'
                    elif field.aggregation is not None and isinstance(field.aggregation, SQLFunction):
                        string = '"' + field.aggregation.name + " " + field.column + '"'
                    else:
                        string = '"' + field.column + '"'
                else:
                    if field.aggregation is not None and isinstance(field.aggregation, str):
                        string = '"' + field.aggregation + " " + field.column + " AS " + field.alias + '"'
                    elif field.aggregation is not None and isinstance(field.aggregation, SQLFunction):
                        string = '"' + field.aggregation.name + " " + field.column + " AS " + field.alias + '"'
                    else:
                        string = '"' + field.column + " AS " + field.alias + '"'
            fields.append(string)
        spell_str += ", ".join(fields) + "]"

        if self.datasets is not None and self.datasets:
            spell_str += ', "from":["{table}"]'

        if self.where is not None and self.where:
            spell_str += ', "where":['
            condition_str = self._where_spell_out(self.where)
            condition_str = ['"' + cond + '"' for cond in condition_str]
            spell_str += ", ".join(condition_str) + "]"

        if self.groupBy is not None and self.groupBy:
            spell_str += ', "group_by":['
            groupby_vec = []
            for clause in self.groupBy:
                if clause.field.alias is not None:
                    groupby_vec.append(clause.field.alias)
                else:
                    groupby_vec.append(clause.field.column)
            spell_str += ", ".join(groupby_vec) + "]"

        if self.orderBy is not None and self.orderBy:
            spell_str += ', "order_by":['
            orderby_vec = []
            for clause in self.orderBy:
                if isinstance(clause.order, SQLSorting):
                    orderby_vec.append('"' + clause.field + " " + clause.order.name + '"')
                else:
                    orderby_vec.append('"' + clause.field + " " + clause.order + '"')
            spell_str += ", ".join(orderby_vec) + "]"

        if self.limit is not None:
            spell_str += ', "limit": ' + str(self.limit)

        if add_offset:
            if self.offset is not None:
                spell_str += ', "offset": ' + str(self.offset)
            else:
                spell_str += ', "offset": 0'

        spell_str += "}"
        return spell_str


@dataclass
class SmartQuery:
    queries: List[Query]
    components: Optional[List[Union[ChartComponent, MapComponent, QueryComponent, Component]]] = None
    javascript: Optional[List[str]] = None

    def spell_out(self, add_offset=True):
        spell_array = []
        for query in self.queries:
            spell = query.spell_out(add_offset)
            spell_array.append(spell)
        return spell_array

    @staticmethod
    def _get_tokens():
        f = open(os.path.join(os.path.dirname(__file__), "askdata_config", "compression_tokens.json"))
        comp_tokens = json.load(f)
        f.close()
        return comp_tokens

    @staticmethod
    def compress(smartquery_json: str):
        comp_tokens = SmartQuery._get_tokens()
        for token in comp_tokens:
            extended = token['decode']
            code = token['code']
            if extended in smartquery_json:
                smartquery_json = re.sub(r"\b" + extended + r"\b", code, smartquery_json)
        return smartquery_json

    @staticmethod
    def decompress(smartquery_json: str):
        comp_tokens = SmartQuery._get_tokens()
        for token in comp_tokens:
            code = token['code']
            decode = token['decode']
            if code in smartquery_json:
                smartquery_json = re.sub(r"\b" + code + r"\b", decode, smartquery_json)
        return smartquery_json
