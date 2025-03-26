package main

import (
	"io"
	"log"
	"os"

	"github.com/moevm/qemu-riscv-cluster/internal/manager"
)

/*
this is temporary example,
there will be no function declaration in main
of course
*/

func readBinary(filepath string) []byte {
	f, err := os.Open(filepath)
	if err != nil {
		log.Fatalln(err)
	}
	defer f.Close()
	dump := make([]byte, 0)
	for {
		buff := make([]byte, 1024)
		_, err := f.Read(buff)
		dump = append(dump, buff...)
		if err == io.EOF {
			break
		}
	}
	return dump
}

func main() {
	// temporary example main function with 3 tasks
	binary1Path := "../../binary_trash/trash_1"
	binary2Path := "../../binary_trash/trash_2"
	binary3Path := "../../binary_trash/trash_3"
	taskSlice := make([]manager.Task, 3)
	taskSlice[0] = *manager.NewTask("task_1", readBinary(binary1Path))
	taskSlice[1] = *manager.NewTask("task_2", readBinary(binary2Path))
	taskSlice[2] = *manager.NewTask("task_3", readBinary(binary3Path))
	manager.SwarmInit(taskSlice)
}
