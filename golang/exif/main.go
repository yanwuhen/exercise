package main

import (
  "fmt"
  "github.com/xiam/exif"
)

func main() {
    data, _:= exif.Read("/mnt/Z7Z8/1022/recup_dir.26/f342194432.jpg")
    for key, val := range data.Tags {
        fmt.Printf("%s = %s\n", key, val)
    }
}
