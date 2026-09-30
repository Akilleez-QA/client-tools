def undefined_symbols(text):
    symbols=[]
    for line in text.splitlines():
        if '|' not in line:continue
        prefix,suffix=line.split('|',1)
        if 'UNDEF' not in prefix.split():continue
        tokens=suffix.strip().split()
        if tokens:symbols.append(tokens[0])
    return symbols

def has_required(symbols,prefixes):
    return all(any(symbol.startswith(prefix) for symbol in symbols) for prefix in prefixes)

def no_miles_imports(symbols):
    return not any('AIL_' in symbol for symbol in symbols)
