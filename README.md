# CreateThumbnailsForVideo

Скрипт делает 12 обхорных превью по видео в каталоге и сохраняет превью jpg рядом файлом видео, имена файлов совпадают.

Минус текущего релиза: всегда перезаписывает превью, даже если оно уже есть для этого видео.
Решение: необходимо перед созданием превью поискать jpg файл с таким же именем, если найден пропускать.
