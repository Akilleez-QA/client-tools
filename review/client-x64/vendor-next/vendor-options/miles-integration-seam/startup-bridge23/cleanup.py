"""Independent best-effort cleanup; no vendor or subprocess policy inside."""
def cleanup(terminate, unload, defaults, write, result):
    result['cleanup_errors'] = []
    for name, action in [('terminate', terminate), ('unload', unload), ('defaults', defaults)]:
        try:
            value = action()
            if name == 'defaults':
                result['defaults_after'] = value
                result['defaults_unchanged'] = result['defaults_before'] == value
        except Exception as error:
            result['cleanup_errors'].append({'stage': name, 'type': type(error).__name__, 'message': str(error)})
    # Writing is independently attempted even if all cleanup stages fail.
    write(result)
