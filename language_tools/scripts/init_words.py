from words.models import ProviderModel, WordInfoModel

# move data

# load sql

# check data

# init translate provier
if not ProviderModel.objects.filter(name_en="youdao").exists():
    ProviderModel.objects.create(**{
        "name_en":"youdao",
        "name":"xx"
    })