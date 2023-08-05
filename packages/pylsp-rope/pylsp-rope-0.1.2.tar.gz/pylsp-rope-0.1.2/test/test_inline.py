from pylsp_rope import plugin, commands
from pylsp_rope.text import Range
from test.conftest import fixtures_dir, create_document
from test.helpers import (
    assert_changeset,
    assert_code_actions_do_not_offer,
    assert_single_document_edit,
)


def test_inline(config, workspace, code_action_context):
    document = create_document(workspace, "simple_extract_method.py")
    line = 6
    start_col = end_col = document.lines[line].index("extracted_method")
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected = {
        "title": "Inline method/variable",
        "kind": "refactor.inline",
        "command": {
            "command": commands.COMMAND_REFACTOR_INLINE,
            "arguments": {
                "document_uri": document.uri,
                "position": selection["start"],
            },
        },
    }

    assert expected in response

    command = expected["command"]["command"]
    arguments = expected["command"]["arguments"]

    response = plugin.pylsp_execute_command(
        config=config,
        workspace=workspace,
        command=command,
        arguments=arguments,
    )

    edit_request = workspace._endpoint.request.call_args

    document_changeset = assert_single_document_edit(edit_request, document)
    new_text = assert_changeset(document_changeset, target=fixtures_dir / "simple.py")
    assert "extracted_method" not in new_text


def test_inline_not_offered_when_selecting_unsuitable_range(
    config, workspace, code_action_context
):
    document = create_document(workspace, "simple_extract_variable.py")
    line = 4
    start_col = end_col = document.lines[line].index("stdin")
    selection = Range((line, start_col), (line, end_col))

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    assert_code_actions_do_not_offer(
        response,
        command=commands.COMMAND_REFACTOR_INLINE,
    )
