// Request the user's location only after pressing Enable.
async function getUserLocation() {
  if (!navigator.geolocation) {
    document.getElementById("mapStatus").textContent = "Geolocation is not available.";
    return;
  }
  navigator.geolocation.getCurrentPosition(async ({coords}) => {
    try {
      const response = await fetch("/recommendations", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({lat: coords.latitude, lng: coords.longitude})
      });
      if (!response.ok) throw new Error("Recommendations unavailable (" + response.status + ")");
      const results = await response.json();
      if (!window.google || !google.maps) throw new Error("Google Maps browser key is missing");
      const center = {lat: coords.latitude, lng: coords.longitude};
      const map = new google.maps.Map(document.getElementById("googleMap"), {center, zoom: 12});
      new google.maps.Marker({position: center, map, title: "Your location"});
      const bounds = new google.maps.LatLngBounds();
      bounds.extend(center);
      for (const place of results) {
        const pos = {lat: Number(place.lat), lng: Number(place.long)};
        if (!Number.isFinite(pos.lat) || !Number.isFinite(pos.lng)) continue;
        new google.maps.Marker({position: pos, map, title: String(place.locationName)});
        bounds.extend(pos);
      }
      if (results.length) map.fitBounds(bounds);
      document.getElementById("mapStatus").textContent = results.length + " nearby suggestions";
    } catch (err) {
      document.getElementById("mapStatus").textContent = err.message;
    }
  }, () => {
    document.getElementById("mapStatus").textContent = "Location permission was not granted.";
  }, {timeout: 10000, maximumAge: 0});
}
