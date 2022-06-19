from django.core.cache import cache

def cache_or_retrieve(holder:int or str,name:str, model_class ):
    
    key = f"{holder}:{name}"
    obj = cache.get(key,None)
    if obj:
        return obj
    obj = model_class.objects.get(id=holder)
    save = cache.set(key, obj)
    return obj