# EmoRecom

Legacy webcam emotion classification and Google Places recommendations. **Local research/demo only; not ready for public deployment.** The old Google API keys committed to this repository are compromised and must be revoked in Google Cloud. Removing the values from the current files does not erase Git history or copies.

## Security constraints
- Start only on `127.0.0.1`; Flask's debugger and reloader are disabled.
- Camera and location responses are local-only as an interim control, **not** production authentication. Do not expose this server on a shared or public network, including through a reverse proxy.
- The browser requests geolocation **only when the user presses Enable**. Recommendations are computed using the provided coordinates without writing them to disk. Do not add logging of coordinates without privacy review.
- Server-side Google Places and browser-side Google Maps use different keys. Restrict the server key to necessary APIs and appropriate source network restrictions; restrict the browser key by authorized HTTP referrers and Maps JavaScript API. Set quotas/billing alerts.
- Real facial imagery and derived emotion are sensitive. Production requires access control, user consent, retention policy, and review of model limitations.

## Requirements and compatibility
- Python **3.11 is the proposed migration target**, not yet validated for this repository.
- `requirements.txt` is a compatibility candidate, **not a lockfile**. Test and lock versions in a clean environment before deployment.
- Local webcam and OpenCV-compatible hardware.
- Actual model assets: `models/face_hyperparams.xml` and `models/Xception_mini106.hdf5`. Existing placeholder files are insufficient. Obtain trustworthy model weights and validate origin, checksums, preprocessing and output labels; do not download unknown model files or unpickle untrusted weights.
- The standalone `fer_engine/real_time_classifier.py` has not been modernized and may need separate dependencies/model files.

## Local setup
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with **new** restricted credentials. `.env` is gitignored and **not automatically loaded** by the app. Load it into the process environment using your preferred local secret loader, or export the variables directly:
```bash
export GOOGLE_PLACES_API_KEY='your-new-server-key'
export GOOGLE_MAPS_BROWSER_KEY='your-new-browser-key'
python server.py
```

Open http://127.0.0.1:5000/start. Open `/map`, then press **Enable** to consent to location. The app does not automatically run the old `./whereami` binary. Missing keys cause the map route to return 503. Webcam setup failures will raise a descriptive error; model files must be real.

## Configuration
| Environment variable | Meaning |
| --- | --- |
| `GOOGLE_PLACES_API_KEY` | Server Places API key; never expose in HTML or JS |
| `GOOGLE_MAPS_BROWSER_KEY` | Referrer-restricted browser Maps JavaScript key |
| `CAMERA_INDEX` | Device index; defaults to `0` |

## Deployment
**Do not use `python server.py` as a production deployment procedure.** The local-only request guard is a temporary safeguard, not full authentication. Before hosting this app, add real authentication/authorization, TLS, CSRF protection where applicable, per-user state and camera isolation, rate limiting and concurrency controls; remove remaining global mutable state and synchronous external API calls. Validate and pin dependencies and model artifacts. Never enable Flask debug in production.

## Incident response and verification
1. Revoke both formerly embedded keys; issue new separately restricted replacements, and inspect usage/billing.
2. Search the **full Git history**, forks, tags, workflows, artifacts, and logs for keys. Remove leaked history only after coordinating with collaborators; rotation is still mandatory.
3. Use `gitleaks git --redact` for local history scanning and `gitleaks dir .` for working tree scanning; retain secure reports. The CI history scan is expected to fail until legacy exposures in history have been addressed.
4. Run `python -m compileall -q server.py simpserver.py recomendationMonkie` and `python -m pip_audit` (after installing `pip-audit`). Run integration tests with actual webcam/model and a test Google Cloud project before declaring deployment safe.
5. Confirm that no files contain embedded Google keys or `debug=True`, and that no server key is rendered in browser responses.

## Known limitations
The application is legacy research code. Migration to newer TensorFlow/Keras, Google Places API, and dependency versions remains to be verified in an actual environment. Camera streaming and recommendation logic have not been load tested. Do not interpret emotion predictions as clinical assessments.
