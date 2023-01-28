import dialogflow

def detect_intent_text(project_id,session_id,text,language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text= text,language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)

    query_text = response.query_result.query_text
    intent = response.query_result.intent.display_name
    fulfillment = response.query_result.fulfillment_text
    print(intent)
    print(fulfillment)
    return query_text, intent, fulfillment


def detect_entity_value(project_id,session_id, text,language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id,session_id)
    text_input = dialogflow.types.TextInput(text=text,language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    entity = response.query_result.parameters
    entity_values = entity.values()

