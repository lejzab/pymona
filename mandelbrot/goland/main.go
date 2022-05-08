package main

import (
	rand2 "crypto/rand"
	"encoding/binary"
	"fmt"
	"image"
	"image/color"
	"image/png"
	"log"
	"math/cmplx"
	"math/rand"
	"os"
)

const (
	MIN_X_VAL = -2.0
	MAX_X_VAL = 0.6
	MIN_Y_VAL = -1.3
	MAX_Y_VAL = 1.3
	MAX_ITER  = 250
	IMG_WIDTH = 1000
)

type Point struct {
	X int
	Y int
}

func Mandelpoint(x float64, y float64) int {
	z := complex(0.0, 0.0)
	c := complex128(complex(x, y))
	for i := 0; i < MAX_ITER; i++ {
		if cmplx.Abs(z) > 2 {
			return i
		}
		z = z*z + c
	}
	return 0
}

func Mandelbrot(startPoint Point, stopPoint Point, stepX float64, stepY float64) [][]int {
	dx := stopPoint.X - startPoint.X
	dy := stopPoint.Y - startPoint.Y
	var points = make([][]int, dy)
	for i := range points {
		points[i] = make([]int, dx)
	}
	yp := MIN_Y_VAL + float64(startPoint.Y)*stepY
	for j := startPoint.Y; j < stopPoint.Y; j++ {
		xp := MIN_X_VAL + float64(startPoint.X)*stepX
		for i := startPoint.X; i < stopPoint.X; i++ {
			points[i][j] = Mandelpoint(xp, yp)
			xp += stepX
		}
		yp += stepY
	}
	log.Println("and it's gone")
	return points
}

func MakeImage(points [][]int) {
	bounds := image.Rect(0, 0, len(points), len(points[0]))
	myImg := image.NewGray16(bounds)
	for x := 0; x < len(points); x++ {
		for y := 0; y < len(points[0]); y++ {
			p := uint16(points[x][y] * 255)
			myImg.Set(x, y, color.Gray16{p})
		}
	}
	imageName := fmt.Sprintf("pictures/mandelgo_%d.png", rand.Int())
	out, err := os.Create(imageName)
	if err != nil {
		log.Println(err)
	}
	err = png.Encode(out, myImg)
	if err != nil {
		log.Println(err)
	}
	_ = out.Close()
}

func main() {
	log.Println("no cześć")
	b := make([]byte, 8)
	_, err := rand2.Read(b)
	if err != nil {
		log.Println("error:", err)
		return
	}
	rand.Seed(int64(binary.LittleEndian.Uint64(b)))
	stepX := (MAX_X_VAL - MIN_X_VAL) / IMG_WIDTH
	stepY := (MAX_Y_VAL - MIN_Y_VAL) / IMG_WIDTH
	log.Printf("steps: x=%v y=%v", stepX, stepY)
	points := Mandelbrot(Point{0, 0}, Point{IMG_WIDTH, IMG_WIDTH}, stepX, stepY)
	MakeImage(points)
	log.Println("papa biedaczyska")
}
