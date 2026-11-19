import json
from pathlib import Path
import yaml

root = Path.cwd()
source = yaml.safe_load((root / 'work/clash-source.yaml').read_text(encoding='utf-8-sig'))
# Tests only need names and metadata; do not copy subscription credentials.
(root / 'work/config-test.json').write_text(json.dumps(source, ensure_ascii=False), encoding='utf-8')
voice = json.loads((root / 'work/chatgpt-voice.json').read_text(encoding='utf-8-sig'))
suffixes = ['chatgpt.com', 'openai.com', 'oaistatic.com', 'oaiusercontent.com', 'oaistatsig.com', 'openaimerge.com', 'ct.sendgrid.net', 'intercom.io', 'intercomcdn.com']
hosts = ['cdn.workos.com', 'challenges.cloudflare.com', 'forwarder.workos.com', 'frontend-apps-multi-region.workos.com', 'humb.apple.com', 'images.workoscdn.com', 'js.stripe.com', 'o207216.ingest.sentry.io', 'o33249.ingest.sentry.io', 'rum.browser-intake-datadoghq.com', 'setup.workos.com', 'workos.imgix.net']
# Preserve additional OpenAI destinations already identified by this subscription.
extra = []
for rule in source['rules']:
    parts = rule.split(',')
    if len(parts) >= 3 and 'openai' in parts[1] and parts[0] in ('DOMAIN', 'DOMAIN-SUFFIX'):
        if parts[1] == 'openai.com' or parts[1].endswith('.openai.com'):
            continue
        extra.append(','.join(parts[:2]))
matches = list(dict.fromkeys(['DOMAIN-SUFFIX,' + x for x in suffixes] + ['DOMAIN,' + x for x in hosts] + extra))
prefixes = [entry.get('ipv4Prefix') or entry.get('ipv6Prefix') for entry in voice['prefixes']]
script = '''// FlClash：当前订阅 → 扩展 → 脚本。
// 仅追加一个组，并在原规则之前添加 ChatGPT 相关规则。
// 美国节点按订阅名称中的“美国”识别，不能据此验证实际出口地区。
function main(config) {
  const groupName = "🤖 ChatGPT 美国";
  const usNodes = (config.proxies || [])
    .filter(p => typeof p.name === "string" && p.name.includes("美国"))
    .map(p => p.name);
  // 若订阅以后删除全部美国节点，阻断这些连接，避免改走其他地区。
  const group = { name: groupName, type: "select", proxies: usNodes.length ? usNodes : ["REJECT"] };
  const oldGroups = config["proxy-groups"] || [];
  const existing = oldGroups.find(g => g.name === groupName);
  if (existing && JSON.stringify(existing) !== JSON.stringify(group)) {
    throw new Error("已有同名组，请修改此脚本中的 groupName，避免覆盖原组。");
  }

  // OpenAI 网络文档列出的域名，以及原订阅的相关辅助域名。
  // 共享的验证码、客服、登录等域名也会走此组。
  const domainMatches = __MATCHES__;
  // OpenAI 官方语音 IP 快照；更新时间：__VOICE_DATE__。
  // 来源：https://openai.com/chatgpt-voice.json；未来可能变化。
  const voicePrefixes = __PREFIXES__;
  const addedRules = domainMatches.map(r => r + "," + groupName)
    .concat(voicePrefixes.map(ip =>
      (ip.includes(":") ? "IP-CIDR6," : "IP-CIDR,") + ip + "," + groupName + ",no-resolve"
    ));
  const oldRules = config.rules || [];
  // 原规则逐条保留且相对顺序不变；重复执行时不重复添加前缀。
  const alreadyAdded = addedRules.every((rule, i) => oldRules[i] === rule);
  return Object.assign({}, config, {
    "proxy-groups": existing ? oldGroups : oldGroups.concat([group]),
    rules: alreadyAdded ? oldRules : addedRules.concat(oldRules)
  });
}
'''.replace('__MATCHES__', json.dumps(matches, ensure_ascii=False, indent=4)).replace('__PREFIXES__', json.dumps(prefixes, indent=4)).replace('__VOICE_DATE__', voice['creationTime'])
out = root / 'outputs'
out.mkdir(exist_ok=True)
(out / 'FlClash-ChatGPT-US.js').write_text(script, encoding='utf-8')
print(json.dumps({'domain_rules': len(matches), 'voice_ip_rules': len(prefixes), 'us_node_count': sum('美国' in p['name'] for p in source['proxies'])}))
