package worker

import (
	"crypto/md5"
	"fmt"
	"log"
	"net"
	"os"
)

func ByteSliceToInt(slice []byte) int {
	var num int
	num += int(slice[3])
	num = num << 8
	num += int(slice[2])
	num = num << 8
	num += int(slice[1])
	num = num << 8
	num += int(slice[0])
	return num
}

func DoTask(c net.Conn) {
	fmt.Println("worker do task...")
	defer c.Close()
	lenBuf := make([]byte, 4)
	_, err := c.Read(lenBuf)
	if err != nil {
		log.Fatalln(err)
	}
	fileDump := make([]byte, ByteSliceToInt(lenBuf))
	_, err = c.Read(fileDump)
	if err != nil {
		log.Fatalln(err)
	}
	md5Sum := md5.Sum(fileDump)
	c.Write(md5Sum[:])
	fmt.Println("task complete")
}

func Start() {
	socketPath := "/tmp/socket/socket.sock"
	if err := os.RemoveAll(socketPath); err != nil {
		log.Fatalln(err)
	}
	listener, err := net.Listen("unix", socketPath)
	if err != nil {
		log.Fatalln(err)
	}
	defer listener.Close()
	fmt.Println("worker start listen...")
	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Fatalln(err)
		}
		go DoTask(conn)
	}
}
