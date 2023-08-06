from __future__ import annotations

from typing import Any, Set
from uuid import UUID

from braid_db import BraidDB, BraidRecord
from braid_db.models import (
    BraidInvalidationAction,
    BraidInvalidationModel,
    BraidRecordModel,
)


def quote_str(s: Any) -> str:
    return '"' + str(s) + '"'


def node_name_for_record(record: BraidRecord) -> str:
    return f"record{record.record_id}"


def node_name_for_invalidation_action(
    invalidation_action: BraidInvalidationAction,
) -> str:
    return f"invalidation_action{str(invalidation_action.id)[:5]}"


def node_name_for_invalidation(
    invalidation: BraidInvalidationModel | UUID,
) -> str:
    if isinstance(invalidation, BraidInvalidationModel):
        the_id = invalidation.id
    else:
        the_id = invalidation
    return f"invalidation{str(the_id)[:5]}"


def truncate_val(val: Any, max_len: int, from_right=False) -> str:
    str_val = str(val)
    # return str_val

    if len(str_val) > max_len:
        if from_right:
            str_val = "..." + str_val[-max_len:]
        else:
            str_val = str_val[0:max_len] + "..."
    return str_val


def node_shape(node_name: str, shape: str, color: str, label: str) -> str:
    return (
        f'{node_name} [shape={shape}, style=filled, fillcolor="{color}", '
        f'label="{label}"];\n'
    )


def edge_def(
    source_node: str,
    dest_node: str,
    style: Optional[str] = None,
    label: Optional[str] = None,
) -> str:
    attrs = []
    if style is not None:
        attrs.append(f"style={style}")
    if label is not None:
        attrs.append(f'label="{label}"')
    if attrs:
        attr_str = "[" + ", ".join(attrs) + "]"
    else:
        attr_str = ""
    return f"{source_node} -> {dest_node} {attr_str};"


def record_to_dot_shape(record: BraidRecordModel) -> str:
    node_name = node_name_for_record(record)
    if record.invalidation is None:
        color = "yellow"
    else:
        color = "pink"
    return node_shape(node_name, "box", color, record.name)


def invalidation_action_to_dot_shape(
    invalidation_action: BraidInvalidationAction,
) -> str:
    node_name = node_name_for_invalidation_action(invalidation_action)
    return node_shape(node_name, "hexagon", "green", invalidation_action.name)


def invalidation_to_dot_shape(invalidation: BraidInvalidationModel) -> str:
    node_name = node_name_for_invalidation(invalidation)
    node = node_shape(node_name, "parallelogram", "violet", invalidation.cause)
    to_root = ""
    if invalidation.root_invalidation is not None:
        root_node_name = node_name_for_invalidation(
            invalidation.root_invalidation
        )
        to_root = edge_def(root_node_name, node_name, label="Causes")
    return node + to_root


def to_dot(root_record_id: int, DB: BraidDB) -> str:
    visited: Set[int] = set()
    graph_def = "digraph G {\n"
    session = DB.get_session()

    record = DB.get_record_model_by_id(root_record_id, session=session)
    to_visit = [record]
    while len(to_visit) > 0:
        record = to_visit.pop()
        rec_node_name = node_name_for_record(record)
        graph_def += record_to_dot_shape(record)
        visited.add(record.record_id)

        if record.invalidation_action is not None:
            graph_def += invalidation_action_to_dot_shape(
                record.invalidation_action
            )
            action_node_name = node_name_for_invalidation_action(
                record.invalidation_action
            )
            graph_def += edge_def(
                action_node_name, rec_node_name, style="dotted"
            )

        if record.invalidation is not None:
            graph_def += invalidation_to_dot_shape(record.invalidation)
            invalidation_node_name = node_name_for_invalidation(
                record.invalidation
            )
            graph_def += edge_def(
                invalidation_node_name,
                rec_node_name,
                style="dotted",
                label="Invalidates",
            )

        derivatives = DB.get_derivations(record.record_id, session)

        for derivative in derivatives:
            deriv_node_name = node_name_for_record(derivative)
            graph_def += f"{rec_node_name}->{deriv_node_name}\n"
            if (
                derivative.record_id not in visited
                and derivative not in to_visit
            ):
                to_visit.append(derivative)

        predecessors = DB.get_predecessors(record.record_id, session)
        for pred in predecessors:
            if pred.record_id not in visited and pred not in to_visit:
                to_visit.append(pred)
    session.close()
    graph_def += "\n}\n"
    return graph_def


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("record_id", type=int)
    parser.add_argument("--db-file", type=str, required=True)

    args = parser.parse_args()

    DB = BraidDB(args.db_file)

    dot_graph = to_dot(args.record_id, DB)

    sys.stdout.write(dot_graph)
