package manager

import (
	"fmt"
	"log"
	"net"
	"time"
)

type Task struct {
	name  string
	state string
	body  []byte
	solve []byte
}

type Worker struct {
	socketPath    string
	taskReceived  int
	taskSend      int
	taskInputChan chan *Task
}

func (t Task) String() string {
	return fmt.Sprintf("Task name:%v, status:%v, solution:%v", t.name, t.state, t.solve)
}

func IntToByteSlice(num int) []byte {
	slice := []byte{}
	slice = append(slice, byte(num>>0))
	slice = append(slice, byte(num>>8))
	slice = append(slice, byte(num>>16))
	slice = append(slice, byte(num>>24))
	return slice
}

func (w *Worker) AddTask(task *Task) {
	if len(w.socketPath) == 0 || w.taskInputChan == nil {
		log.Fatalln("worker is broken")
	}
	if task.body == nil {
		log.Fatalln("task is empty")
	}
	var err error
	var openConnection net.Conn
	openConnection, err = net.Dial("unix", w.socketPath)
	if err != nil {
		log.Fatalln(err)
	}
	defer openConnection.Close()
	if _, err = openConnection.Write(IntToByteSlice(len(task.body))); err != nil {
		log.Fatalln(err)
	}
	if _, err = openConnection.Write(task.body); err != nil {
		log.Fatalln(err)
	}
	w.taskSend += 1
	task.state = "wip"
	buf := make([]byte, 16)
	_, err = openConnection.Read(buf)
	task.solve = append(task.solve, buf...)
	if err != nil {
		log.Fatalln(err)
	}
	w.taskReceived += 1
	task.state = "solved"
}

func (w *Worker) Run() {
	for {
		task := <-w.taskInputChan
		go w.AddTask(task)

	}
}

func NewWorker(target string, inputChannel chan *Task) *Worker {
	return &Worker{
		socketPath:    target,
		taskInputChan: inputChannel,
	}
}

func NewTask(taskName string, taskBody []byte) *Task {
	return &Task{
		name:  taskName,
		state: "created",
		body:  taskBody,
		solve: make([]byte, 0),
	}
}

func SwarmInit(tasks []Task) {
	// temporary example with solo worker and predetermined tasks
	socketPath := "/tmp/socket/socket.sock"
	taskChannel := make(chan *Task, 4)
	worker1 := NewWorker(socketPath, taskChannel)
	go worker1.Run()
	for i := range tasks[:3] {
		taskChannel <- &tasks[i]
	}
	for {
		for i := range tasks {
			fmt.Println(tasks[i])
			time.Sleep(350 * time.Millisecond)
		}
	}
}
