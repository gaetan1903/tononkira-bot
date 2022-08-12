FROM ghcr.io/iteam-s/ampalibe

ADD . /usr/src/app/

CMD ampalibe -p $PORT run