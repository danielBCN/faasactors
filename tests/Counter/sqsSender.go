package main

import (
	"fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sqs"
	"os"
	"sync"
	"time"
)

func main(){
	fmt.Print("Hello World!", os.Args[1])


	sess := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))

	svc := sqs.New(sess)

	// URL to our queue
	qURL := os.Args[2]

	var wg sync.WaitGroup
	wg.Add(100)
	start := time.Now()
	for i := 0; i < 100; i++ {
		go func() {
			svc.SendMessage(&sqs.SendMessageInput{MessageBody: aws.String(os.Args[1]),QueueUrl:&qURL,})
			svc.SendMessage(&sqs.SendMessageInput{MessageBody: aws.String(os.Args[1]),QueueUrl:&qURL,})
			svc.SendMessage(&sqs.SendMessageInput{MessageBody: aws.String(os.Args[1]),QueueUrl:&qURL,})

			svc.SendMessage(&sqs.SendMessageInput{MessageBody: aws.String(os.Args[1]),QueueUrl:&qURL,})
			svc.SendMessage(&sqs.SendMessageInput{MessageBody: aws.String(os.Args[1]),QueueUrl:&qURL,})
			svc.SendMessage(&sqs.SendMessageInput{MessageBody: aws.String(os.Args[1]),QueueUrl:&qURL,})

			svc.SendMessage(&sqs.SendMessageInput{MessageBody: aws.String(os.Args[1]),QueueUrl:&qURL,})
			svc.SendMessage(&sqs.SendMessageInput{MessageBody: aws.String(os.Args[1]),QueueUrl:&qURL,})
			svc.SendMessage(&sqs.SendMessageInput{MessageBody: aws.String(os.Args[1]),QueueUrl:&qURL,})

			wg.Done()
		}()
	}
	wg.Wait()
	fmt.Println(time.Since(start))
	fmt.Println("end")
}
