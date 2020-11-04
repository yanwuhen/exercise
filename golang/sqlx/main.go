package main

import (
	"encoding/json"
	"log"

	//go sql driver: https://github.com/golang/go/wiki/SQLDrivers
	//_ "github.com/go-sql-driver/mysql" 
	_ "github.com/mattn/go-sqlite3"
	"github.com/jmoiron/sqlx"
)

// Customer ...
type Customer struct {
	Id      int    `db:"id"`
	Name    string `db:"name"`
	OrderId *int   `db:"order_id"` //如果为int则select会忽略null的记录
}

func main() {
	//db, err := sqlx.Open("mysql", "user:passwd@tcp(ip:port)/db?charset=utf8")
	db, err := sqlx.Open("sqlite3", "./test.db")
	_ = db
	if err != nil {
		log.Print()
	}

	arr := []Customer{}
	err = db.Select(&arr, "SELECT id,name,order_id FROM person")
	if err != nil {
		log.Print("query failed", err)
	}
	//log.Printf("%v", arr)

	buf, err := json.MarshalIndent(arr, "", "\t")
	log.Printf("\n%s", buf)
}
