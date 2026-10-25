package alerts

// User is someone who receives alerts.
type User struct {
	ID          int
	Email       string
	Phone       string // empty when the user gave none
	DeviceToken string // empty when the user has not installed the app
}
