package main

import (
	"flag"
	"fmt"
	"github.com/go-redis/redis"
	"io/ioutil"
	"log"
	"os"
	"sync"
	"syscall"
	"time"
)

type FileStat struct {
	Id       int    `db:"id"`
	Name     string `db:"name"`
	Size     int64
	Atime    time.Time
	Mtime    time.Time
	Ctime    time.Time
	Parentid int
}

var client *redis.Client

var ch chan string

func main() {
	log.Println("start")
	defer log.Println("end")
	path := flag.String("n", "", "path")
	conc := flag.Int("c", 100, "concurrent")
	poolMax := flag.Int("p", 100, "thread pool")
	flag.Parse()
	if path == nil || *path == "" {
		log.Panicln("pls input filename")
	}

	client = redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "",
		DB:       0,
	})
	defer client.Close()
	pong, err := client.Ping().Result()
	if err != nil {
		log.Panicln("open redis failed:", pong)
	}

	ch = make(chan string, *conc)
	var wg sync.WaitGroup
	for i := 0; i < *poolMax; i++ {
		wg.Add(1)
		go proc(&wg)
	}
	listAllFile(*path)
	close(ch)
	wg.Wait()
}

func listAllFile(rootDir string) {
	rd, err := ioutil.ReadDir(rootDir)
	if err != nil {
		log.Println("read dir failed", err)
		return
	}
	for _, f := range rd {
		filename := fmt.Sprintf("%s/%s", rootDir, f.Name())
		if f.IsDir() {
			listAllFile(filename)
		}
		ch <- filename
	}
}

func proc(waitGroup *sync.WaitGroup) {
	defer waitGroup.Done()
	//log.Println("start goroutine")
	for filename := range ch {
		//log.Println("start work", filename)
		fileinfo, err := os.Stat(filename)
		if err != nil {
			log.Println("stat failed", err)
			continue
		}
		mtime := fileinfo.ModTime()
		stat := fileinfo.Sys().(*syscall.Stat_t)
		atime := time.Unix(int64(stat.Atim.Sec), int64(stat.Atim.Nsec))
		ctime := time.Unix(int64(stat.Ctim.Sec), int64(stat.Ctim.Nsec))
		insertDB(filename, fileinfo.Size(), atime, mtime, ctime, 3)
	}
	//log.Println("end goroutine")
}

func insertDB(filename string, size int64, atime, mtime, ctime time.Time, tryCnt int) {
	statMap := make(map[string]interface{})
	statMap["name"] = filename
	statMap["size"] = size
	statMap["atime"] = atime
	statMap["mtime"] = mtime
	statMap["ctime"] = ctime
	err := client.HMSet(filename, statMap).Err()
	if err != nil {
		/*
		if tryCnt > 0 {
			log.Println(err, "tryCnt =", tryCnt)
			time.Sleep(time.Duration(1) * time.Second)
			insertDB(filename, size, atime, mtime, ctime, tryCnt-1)
			return
		}
		*/
		log.Panicln("insert fail:", err.Error())
	}
}
