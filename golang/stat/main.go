package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
	"sync"
	"syscall"
	"time"

	"github.com/jmoiron/sqlx"
	_ "github.com/go-sql-driver/mysql"
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

var db *sqlx.DB

const CONCURRENT int = 1000 
const THREAD_POOL_MAX int = 150

var ch chan string

func main() {
	path := flag.String("n", "", "path")
	flag.Parse()
	if path == nil || *path == "" {
		log.Panicln("pls input filename")
	}

	var err error
	db, err = sqlx.Open("mysql", "mysql:mysql@/webdb")
	if err != nil {
		log.Panicln("open db failed:", err)
	}
	defer db.Close()

	ch = make(chan string, CONCURRENT)
	var wg sync.WaitGroup
	for i := 0; i < THREAD_POOL_MAX; i++ {
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
	log.Println("start goroutine")
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
	log.Println("end goroutine")
}

func insertDB(filename string, size int64, atime, mtime, ctime time.Time, tryCnt int){
	_, err := db.Exec("insert into allfile(`name`,`size`,atime,mtime,ctime) values(?, ?, ?, ?, ?)", filename, size, atime, mtime, ctime)
		if err != nil {
			if strings.Contains(err.Error(), "locked") && tryCnt>0{
				log.Println(err, "tryCnt =", tryCnt)
				time.Sleep(time.Duration(1) * time.Second)
				insertDB(filename, size, atime, mtime, ctime, tryCnt - 1)
				return
			}
			log.Panicln("insert fail:", err, filename)
		}
}

