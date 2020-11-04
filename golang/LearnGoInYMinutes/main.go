package main

import (
	"fmt"
	"log"
	"sync"
	"time"

	//. "fmt"这么写不需要加包名fmt.Println => Println
	//f "fmt"别名fmt.Println => f.Println
	// _ "xxx"只完成init工作而不实际导入
	"unsafe"
)

//这是一个注释
//go语言圣经：https://books.studygolang.com/gopl-zh/
/*
函数之外的变量，包内可见
但只有大写开头的，才能被包外访问
*/
var gloalA int
var GloalB int

type Point struct {
	x int
	y int
}

func (p *Point) MoveLeft(step int) string {
	//结构体指针的接收器，类似类的方法this->等
	//但结构体的接收器，只是复制值不会真正修改
	p.x -= 1
	return fmt.Sprintf("now in (%d,%d)", p.x, p.y)
}

func main() {
	learnDeclaration() //声明
	learnType()
	learnJson()
	learnFlow()
	learnFunc()
	learnPanic()
	learnGoroutine()
	learnGoLtd()
}

//todo 标准库
func learnGoLtd() {

}

func goroutineExample1() {
	c := make(chan int, 2)
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		i := <-c
		fmt.Println(i)
		//打印12，缓冲区为空时读阻塞，缓冲区满时写阻塞
		//底层数据结构是一个环形队列
		//缓冲区为空，读写都阻塞，可以视为长度0的缓存区
	}()
	c <- 12
	c <- 13
	wg.Wait()
}

func goroutineExample2() {
	c := make(chan int, 3)
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		for i := range c {
			log.Println("pop:", i)
			time.Sleep(time.Second * time.Duration(1))
		}
	}()
	for i := 0; i < 10; i++ {
		c <- i
		log.Println("push:", i)
	}
	close(c)
	wg.Wait()
}

func goroutineExample3() {
	c := make(chan int)
	e := make(chan int)
	go func() {
		i := 0
		for {
			select {
			case c <- i:
				i += 1
			case <-e:
				log.Println("exit")
				return
			default:
				log.Println("dont do anything")
			}
			/*
			select随时执行满足的条件
			条件不满足时，没有default的话阻塞
			有default时执行default
			*/
		}
	}()
	for i := 0; i < 10; i++ {
		a := <-c
		log.Println(a)
	}
	e <- 100
}

func learnGoroutine() {
	fmt.Println("===learnGoroutine===")
	//goroutineExample1() //带缓冲区的channel，sync.WaitGroup的使用
	//goroutineExample2() //range来接收不定数量的channel值
	goroutineExample3() //select来接受多个channel，及不阻塞的实现
}

//todo
func learnPanic() {

}

func variadicParams(args ...interface{}) {
	fmt.Println("1st args =", args[0])
	fmt.Println("2st args =", args[1])
	for _, a := range args {
		fmt.Println("a is ", a)
	}
	fmt.Println(args[0])
}

func add(x int, y int) int { return x + y }

//返回值有变量名的，可以直接return
func sub(x, y int) (z int) { z = x - y; return }

//_代表不使用，zero中没有变量名的同理
func first(x int, _ int) int     { return x }
func zero(int, int) int          { return 0 }
func mutilReturn() (int, string) { return 123, "def" }

func learnFunc() {
	fmt.Println("===learnFunc===")
	add(1, 2)
	sub(1, 2)
	first(1, 2)
	zero(1, 2)
	a, _ := mutilReturn()
	fmt.Println("one return ", a)
	//没有原生支持函数默认值
	variadicParams("testString", "1234243")
}

func learnFlow() {
	fmt.Println("===learnFlow===")
	if true && false || true {
		fmt.Println("true")
	} else if true {
		fmt.Println("true true")
	} else {
		fmt.Println("false")
	}

	//switch case
	x := 1
	switch x {
	case 1:
		//不需要break
		fmt.Println("1")
	case 2, 3:
		fmt.Println("2")
	default:
		fmt.Println("default")
	}

	switch {
	case 0 < x && x <= 10:
		fmt.Println("lg 0")
	case 10 < x && x <= 20:
		fmt.Println("lg 10")
	}

	//for loop
	for {
		break
	}

	for i := 0; i < 10; i++ {
		fmt.Println(i)
	}

	for k, v := range map[string]int{"one": 1, "two": 2} {
		//map遍历顺序不固定，不要在循环期间新增或删除
		fmt.Println(k, v)
	}

	//坑
	r := make([]*Point, 0)
	d := []Point{{1, 2}, {3, 4}, {5, 6}}
	for _, v := range d {
		vv := v //这步不能省略
		r = append(r, &vv)
		/* NOTE:
		v变量地址保持不变
		注意d是否为引用类型，引用类型有：slice,map,interface,func,chan
		非引用类型的话，是值拷贝，否则是地址拷贝
		所以同理struct时v.xx也不能修改
		*/
	}
	for _, v := range r {
		fmt.Println(*v)
	}
	//另外一个例子
	a := [3]int{1, 2, 3}
	for i, v := range a { //i,v从a复制的对象里提取出
		if i == 0 {
			a[1], a[2] = 200, 300
			fmt.Println(a) //输出[1 200 300]
		}
		a[i] = v + 100 //v是复制对象里的元素[1, 2, 3]
	}
	fmt.Println(a) //输出[101, 102, 103]
	//如果a为slice，结果会不一样
}

//todo
func learnJson() {

}

func learnType() {
	fmt.Println("===learnType===")
	s := "sting"
	i := 1
	f := 1.2
	c := 3 + 4i // complex128类型，内部使用两个float64表示
	pi := &i    //指针

	//数组array
	var aa [4]int
	bb := [...]int{1, 2, 3}
	//切片slice
	medals := make([]string, 4)
	medals = []string{"gold", "silver", "bronze"}
	medals = append(medals, "unkown")
	//字典map
	m := map[string]int{"one": 1, "two": 2}
	//结构体
	type S struct {
		Point
		A int
		B string
		C int
	}
	s1 := S{A: 1, B: "2", C: 3} //可以不写成员名字，但结构体顺序变化会出错
	s1.C = 4
	(&s1).C = 5 //结构体指针也使用.不使用->
	s1.x = 0    //Point是匿名成员，可以不写

	p := Point{x: 1, y: 1}
	fmt.Println(p.MoveLeft(1))

	//类型转换,只能是兼容类型,但何为兼容类型还没有找到
	n := byte('\n') // byte是uint8的别名
	var pipi *int64 = (*int64)(unsafe.Pointer(pi))

	//类型断言,x.(T)其中x必须是接口值
	var x interface{}
	x = 10
	value, ok := x.(int) //如果不接收ok，断言失败时会panic
	fmt.Println(value, ok)
	//x.(type),只能配合switch使用
	getType(i)

	//todo
	//reflect type
	fmt.Println("type:", s, i, f, c, aa[0], bb[1], medals, n, m["one"], s1, pipi)
}

func getType(a interface{}) {
	switch a.(type) {
	case int:
		fmt.Println("the type of a is int")
	case string:
		fmt.Println("the type of a is string")
	case float64:
		fmt.Println("the type of a is float")
	default:
		fmt.Println("unknown type")
	}
}

func learnDeclaration() {
	fmt.Println("===learnDeclaration===")
	var a int
	var a1, a2 int
	var b, c = 1, "string"
	d := 3 //简短变量声明
	const e = "eeeee"
	var A *int
	A = &a
	B := &b
	C := new(string)
	fmt.Println("declaration:", a, a1, a2, b, c, d, e, *A, *B, *C)
}
