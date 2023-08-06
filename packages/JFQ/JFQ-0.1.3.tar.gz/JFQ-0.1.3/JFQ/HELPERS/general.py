def list_results(result,tab="___"):
    if not (isinstance(result,list) or isinstance(result,dict) or isinstance(result,tuple)):
        print(tab,result)
        return
    if isinstance(result,list) or isinstance(result,tuple):
        for listElement in result:
            list_results(listElement)
        return
    for key in result:
        value = result[key]
        if isinstance(value,dict):
            print(tab, key)
            newtab=tab+"___"
            list_results(value,newtab)
        elif isinstance(value,list):
            print(tab, key)
            newtab = tab + "___"
            for listElement in value:
                list_results(listElement,newtab)
        else:
            print(tab,key,":",result[key])