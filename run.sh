# docker build -t voting .
docker run -it --rm -v $PWD:/src voting python main.py