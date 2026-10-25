package weather_test

import (
	"context"
	"net/http"
	"net/http/httptest"
	"testing"

	"example.com/weather"
)

func TestFetchReturnsThePayload(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/v1/forecast" || r.URL.Query().Get("city") != "Oslo" {
			http.Error(w, "unexpected request", http.StatusBadRequest)
			return
		}
		w.Write([]byte(`{"daily": [{"pop": 0.7, "tmax": 12.3}]}`))
	}))
	defer server.Close()
	api := &weather.ForecastAPI{BaseURL: server.URL, HTTP: server.Client()}
	payload, err := api.Fetch(context.Background(), "Oslo")
	if err != nil || payload["daily"] == nil {
		t.Fatalf("Fetch = %v, %v; want the daily forecast", payload, err)
	}
}
