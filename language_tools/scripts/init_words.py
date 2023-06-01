from words.models import TranslateProviderModel, TranslateWordDataModel

# move data

# load sql

# check data

# init translate provier
if not TranslateProviderModel.objects.filter(name_en="youdao").exists():
    TranslateProviderModel.objects.create(**{
        "name_en":"youdao",
        "name":"xx"
    })