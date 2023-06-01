from ielts.models import BookModel, ChapterModel, PaperModel, WordModel

BookModel.objects.create(**{"name":"wanglu_tingli","cover":"","description":"1111",})
ChapterModel.objects.create(**{"name":"paper1","book_id_id":"1"})
p =PaperModel.objects.create(**{"name":"paper1","chapter_id":1})
# WordModel.objects.create(**{"name":"corpus","zh":"还好","symbol":"","mp3_file_uuid":"b7d1c94c-d85c-4aa0-8c5a-2444124ad54a"})
w = WordModel.objects.create(**{"name":"corpus"})

p.words.add(w)
