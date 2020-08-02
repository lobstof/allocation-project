# preapre docker images

netflix_server_build:
	docker build -t netflix-server:1.0 ./JSON_server_netflix_image

youtube_server_build:
	docker build -t youtube-server:1.0 ./JSON_server_youtube_image

netflix_cdn_download:
	sh ./cdn_images/download_cdn_netflix_image.sh

youtube_cdn_download:
	sh ./cdn_images/download_cdn_youtube_image.sh

cdn_images_build:
	docker load --input ./cdnyoutube.tar
	docker load --input ./cdnnetflix.tar

docker_image_prepare: netflix_server_build youtube_server_build netflix_cdn_download youtube_cdn_download cdn_images_build