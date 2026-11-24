"""Download PandaOS public reference images into research/reference-images/."""
import os
import urllib.request

BASE = r"C:\Users\naxos\Documents\CapybaraOS\research\reference-images"
os.makedirs(BASE, exist_ok=True)

IMAGES = {
    "01-interface-design.png": "https://pandaos.ai/img/homepage/features/interface-design.png",
    "02-multi-project.webp": "https://pandaos.ai/img/homepage/features/multi-project.webp",
    "03-agent-workflows.webp": "https://pandaos.ai/img/homepage/features/agent-workflows.webp",
    "04-bypass-session-limits.webp": "https://pandaos.ai/img/homepage/features/bypass-session-limits.webp",
    "05-project-memory.webp": "https://pandaos.ai/img/homepage/features/project-memory.webp",
    "06-ai-native-dev-env.webp": "https://pandaos.ai/img/homepage/features/ai-native-dev-env.webp",
    "07-connected-apps.webp": "https://pandaos.ai/img/homepage/features/connected-apps.webp",
    "10-usecase-bug-report.webp": "https://pandaos.ai/img/homepage/use-cases/bug-reports.webp",
    "11-usecase-analytics.webp": "https://pandaos.ai/img/homepage/use-cases/analytics-query.webp",
    "12-usecase-competitive-audit.webp": "https://pandaos.ai/img/homepage/use-cases/competitive-site-audit.webp",
    "13-usecase-standup.webp": "https://pandaos.ai/img/homepage/use-cases/dev-standup-prep.webp",
    "14-usecase-weekly-metrics.webp": "https://pandaos.ai/img/homepage/use-cases/weekly-metrics.webp",
    "15-usecase-failed-deploy.webp": "https://pandaos.ai/img/homepage/use-cases/failed-deployment-fix.webp",
    "16-usecase-hero-live.webp": "https://pandaos.ai/img/homepage/use-cases/update-hero.webp",
    "17-usecase-release-changelog.webp": "https://pandaos.ai/img/homepage/use-cases/release-changelog.webp",
    "20-app-connections.png": "https://yiynfbzujefrgxejlqfo.supabase.co/storage/v1/object/public/docs-media/apps/connecting/authentication.png",
    "21-app-per-tool.png": "https://yiynfbzujefrgxejlqfo.supabase.co/storage/v1/object/public/docs-media/apps/actions-and-permissions/per-tool.png",
    "22-model-connections.png": "https://yiynfbzujefrgxejlqfo.supabase.co/storage/v1/object/public/docs-media/settings/models/connections.png",
    "23-chat-switch-engine.png": "https://yiynfbzujefrgxejlqfo.supabase.co/storage/v1/object/public/docs-media/chat/connections/switching-a-chat.png",
    "24-mobile-pairing.png": "https://yiynfbzujefrgxejlqfo.supabase.co/storage/v1/object/public/docs-media/mobile/overview.png",
}

for name, url in IMAGES.items():
    path = os.path.join(BASE, name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
        print(f"OK   {name:38} {len(data):>9,} bytes")
    except Exception as exc:
        print(f"FAIL {name:38} {exc}")
