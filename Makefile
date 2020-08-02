# preapre docker images

netflix_server_build:
	cd ./JSON_server_netflix_image
	docker -t netflix-server .
	cd ..

youtube_server_build:
	cd ./JSON_server_youtube_image
	docker -t youtube-server .
	cd ..

netflix_cdn_download:
	cd ./cdn_images
	sh download_cdn_netflix_image.sh
	cd ..

youtube_cdn_download:
	cd ./cdn_images
	sh download_cdn_youtube_image.sh
	cd ..

cdn_images_build:
	cd ./cdn_images
	docker load --input cdnyoutube.tar
	docker load --input cdnnetflix.tar
	cd ..

docker_image_prepare: netflix_server_build youtube_server_build netflix_cdn_download youtube_cdn_download cdn_images_build