package weather_test

import (
	"context"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"

	"example.com/weather"
)

// hiddenAPI is the provider answering every request with a fixed payload.
func hiddenAPI(t *testing.T, rainChance float64) *weather.ForecastAPI {
	t.Helper()
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, `{"daily": [{"pop": %v, "tmax": 12.3}, {"pop": 0.0, "tmax": 15.0}]}`, rainChance)
	}))
	t.Cleanup(server.Close)
	return &weather.ForecastAPI{BaseURL: server.URL, HTTP: server.Client()}
}

func TestHiddenUmbrellaAdvice(t *testing.T) {
	for rainChance, want := range map[float64]bool{0.7: true, 0.2: false} {
		got, err := weather.ShouldTakeUmbrella(context.Background(), "Oslo", hiddenAPI(t, rainChance))
		if err != nil || got != want {
			t.Errorf("rain chance %v: ShouldTakeUmbrella = %v, %v; want %v", rainChance, got, err, want)
		}
	}
}
