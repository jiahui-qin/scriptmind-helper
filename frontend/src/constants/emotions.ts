// 单句属性 — 基础情绪
export const BASIC_EMOTIONS = [
  '平静', '开心', '悲伤', '愤怒', '恐惧', '惊讶', '兴奋', '委屈', '冷漠'
];

// 单句属性 — 复合情绪
export const COMPLEX_EMOTIONS = [
  '怅然', '欣慰', '无奈', '愧疚', '释然', '嫉妒', '厌倦', '忐忑', '动情'
];

// 人物属性
export const TONE_STYLES = ['温柔', '高冷', '活泼', '严肃', '慵懒', '俏皮', '深沉', '干练', '凌厉'];
export const VOICE_COLORS = ['磁性', '醇厚', '清亮', '空灵', '稚嫩', '苍老', '甜美', '沙哑', '醇雅'];
export const PERSONA_ACCENTS = ['夹子音', '御姐音', '正太音', '大叔音', '台湾腔'];
export const DIALECTS = ['普通话', '东北话', '四川话', '河南话', '粤语'];
export const ROLEPLAYS = ['无', '孙悟空', '林黛玉'];
export const SINGING_STYLES = ['无', '唱歌'];

// 分类映射 — 用于 API 调用
export const STYLE_CATEGORIES: Record<string, string[]> = {
  emotion_tag: BASIC_EMOTIONS,
  complex_emotion: COMPLEX_EMOTIONS,
  tone_style: TONE_STYLES,
  voice_color: VOICE_COLORS,
  persona_accent: PERSONA_ACCENTS,
  dialect: DIALECTS,
  roleplay: ROLEPLAYS,
  singing: SINGING_STYLES,
};

// 情感标签颜色
export const EMOTION_COLORS: Record<string, string> = {
  '开心': '#22c55e', '悲伤': '#6366f1', '愤怒': '#ef4444', '恐惧': '#a855f7',
  '惊讶': '#f59e0b', '兴奋': '#ec4899', '委屈': '#14b8a6', '平静': '#94a3b8',
  '冷漠': '#6b7280',
  '怅然': '#8b5cf6', '欣慰': '#10b981', '无奈': '#78716c', '愧疚': '#f97316',
  '释然': '#06b6d4', '嫉妒': '#dc2626', '厌倦': '#9ca3af', '忐忑': '#eab308',
  '动情': '#db2777',
};
