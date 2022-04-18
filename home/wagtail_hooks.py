from wagtail.core import hooks
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler

@hooks.register('register_rich_text_features')
def register_code_styling(features):
# Add the code feature to the list of features
  feature_name="code"
  type_="CODE"
  tag="code"

  control ={
    "type": type_,
    "label": "</>",
    "description": "Code",
  }
  features.register_editor_plugin(
    "draftail", feature_name, draftail_features.InlineStyleFeature(control)
  )

  db_conversion ={
    "from_database_format": {tag: InlineStyleElementHandler(type_)},
    "to_database_format": {"Style_map": {type_: {"element": tag}}}
  }

  features.register_converter_rule("contentstate", feature_name, db_conversion)

  # This is the default rule for all features
  features.default_features.append(feature_name)


@hooks.register('register_rich_text_features')
def register_centertext_feature(features):
  # create centered text in the editor panel
  feature_name="centertext"
  type_="CENTER"
  tag="div"

  control ={
    "type": type_,
    "label": "Center",
    "description": "Center Text",
    "style": {
      "dispay": "block",
      "text-align": "center",
    }
  }
  features.register_editor_plugin(
    "draftail", feature_name, draftail_features.InlineStyleFeature(control)
  )

  db_conversion ={
    "from_database_format": {tag: InlineStyleElementHandler(type_)},
    "to_database_format": {"style_map": {
      type_: {
        "element": tag,
        "props": {
          "class": "d-block text-center"
        }
        }
      }
      }
  }

  features.register_converter_rule("contentstate", feature_name, db_conversion)

  # This is the default rule for all features
  features.default_features.append(feature_name)

@hooks.register('bootstrap_after_html_document_ready')
def add_custom_css():
  return """
  <style>
    .d-block {
      display: block;
    }
  </style>
  """