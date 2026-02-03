// AI Tools Database - Phase 69: More Audio & Voice AI
// 100+ Additional audio and voice tools

const AI_TOOLS_PHASE69 = [
    // ==================== TEXT TO SPEECH ====================
    {name: "ElevenLabs", category: "Audio", subcategory: "TTS", desc: "AI voice generation", url: "elevenlabs.io", pricing: "Freemium", rating: 4.7, tags: ["tts", "voice-clone", "realistic"], featured: true},
    {name: "Murf.ai", category: "Audio", subcategory: "TTS", desc: "AI voice generator", url: "murf.ai", pricing: "Freemium", rating: 4.5, tags: ["tts", "voiceover", "studio"]},
    {name: "Play.ht", category: "Audio", subcategory: "TTS", desc: "AI voice generator", url: "play.ht", pricing: "Freemium", rating: 4.4, tags: ["tts", "realistic", "api"]},
    {name: "Resemble.ai", category: "Audio", subcategory: "Voice Clone", desc: "Voice cloning AI", url: "resemble.ai", pricing: "Paid", rating: 4.4, tags: ["voice-clone", "synthetic", "enterprise"]},
    {name: "Speechify", category: "Audio", subcategory: "TTS", desc: "Text to speech", url: "speechify.com", pricing: "Freemium", rating: 4.4, tags: ["tts", "reading", "accessibility"]},
    {name: "LOVO", category: "Audio", subcategory: "TTS", desc: "AI voice & video", url: "lovo.ai", pricing: "Freemium", rating: 4.3, tags: ["tts", "video", "genny"]},
    {name: "Wellsaid Labs", category: "Audio", subcategory: "TTS", desc: "Enterprise TTS", url: "wellsaidlabs.com", pricing: "Paid", rating: 4.3, tags: ["tts", "enterprise", "studio"]},
    {name: "Coqui", category: "Audio", subcategory: "TTS", desc: "Open source TTS", url: "coqui.ai", pricing: "Freemium", rating: 4.3, tags: ["tts", "open-source", "voice-clone"]},
    {name: "Descript Overdub", category: "Audio", subcategory: "Voice Clone", desc: "Voice cloning", url: "descript.com/overdub", pricing: "Paid", rating: 4.4, tags: ["voice-clone", "descript", "editing"]},
    {name: "Listnr", category: "Audio", subcategory: "TTS", desc: "AI voice generator", url: "listnr.tech", pricing: "Freemium", rating: 4.2, tags: ["tts", "podcast", "voiceover"]},
    {name: "Natural Reader", category: "Audio", subcategory: "TTS", desc: "Text to speech", url: "naturalreaders.com", pricing: "Freemium", rating: 4.2, tags: ["tts", "ocr", "accessibility"]},
    {name: "Voicemaker", category: "Audio", subcategory: "TTS", desc: "Online TTS", url: "voicemaker.in", pricing: "Freemium", rating: 4.1, tags: ["tts", "online", "affordable"]},
    {name: "TTSReader", category: "Audio", subcategory: "TTS", desc: "Free text to speech", url: "ttsreader.com", pricing: "Free", rating: 4.0, tags: ["tts", "free", "web"]},
    {name: "Narakeet", category: "Audio", subcategory: "TTS", desc: "Text to video", url: "narakeet.com", pricing: "Paid", rating: 4.1, tags: ["tts", "video", "powerpoint"]},
    
    // ==================== SPEECH TO TEXT ====================
    {name: "AssemblyAI", category: "Audio", subcategory: "STT", desc: "Speech AI API", url: "assemblyai.com", pricing: "Freemium", rating: 4.5, tags: ["stt", "api", "lemur"], featured: true},
    {name: "Deepgram", category: "Audio", subcategory: "STT", desc: "Speech recognition", url: "deepgram.com", pricing: "Freemium", rating: 4.5, tags: ["stt", "api", "real-time"]},
    {name: "Whisper (OpenAI)", category: "Audio", subcategory: "STT", desc: "OpenAI transcription", url: "openai.com/whisper", pricing: "Free", rating: 4.6, tags: ["stt", "open-source", "openai"]},
    {name: "Google Speech-to-Text", category: "Audio", subcategory: "STT", desc: "Google STT API", url: "cloud.google.com/speech-to-text", pricing: "Pay-per-use", rating: 4.4, tags: ["stt", "google", "api"]},
    {name: "AWS Transcribe", category: "Audio", subcategory: "STT", desc: "AWS transcription", url: "aws.amazon.com/transcribe", pricing: "Pay-per-use", rating: 4.3, tags: ["stt", "aws", "api"]},
    {name: "Azure Speech", category: "Audio", subcategory: "STT", desc: "Microsoft speech", url: "azure.microsoft.com/speech", pricing: "Pay-per-use", rating: 4.3, tags: ["stt", "azure", "api"]},
    {name: "Rev.ai", category: "Audio", subcategory: "STT", desc: "Speech recognition API", url: "rev.ai", pricing: "Pay-per-use", rating: 4.3, tags: ["stt", "api", "accurate"]},
    {name: "Speechmatics", category: "Audio", subcategory: "STT", desc: "Speech technology", url: "speechmatics.com", pricing: "Paid", rating: 4.2, tags: ["stt", "enterprise", "multilingual"]},
    {name: "Vosk", category: "Audio", subcategory: "STT", desc: "Offline speech recognition", url: "alphacephei.com/vosk", pricing: "Free", rating: 4.2, tags: ["stt", "offline", "open-source"]},
    
    // ==================== AUDIO EDITING ====================
    {name: "Adobe Podcast", category: "Audio", subcategory: "Editing", desc: "AI audio tools", url: "podcast.adobe.com", pricing: "Free", rating: 4.4, tags: ["editing", "enhance", "free"], featured: true},
    {name: "Descript", category: "Audio", subcategory: "Editing", desc: "Audio/video editor", url: "descript.com", pricing: "Freemium", rating: 4.6, tags: ["editing", "transcription", "video"]},
    {name: "Audacity", category: "Audio", subcategory: "Editing", desc: "Free audio editor", url: "audacityteam.org", pricing: "Free", rating: 4.4, tags: ["editing", "open-source", "desktop"]},
    {name: "Adobe Audition", category: "Audio", subcategory: "Editing", desc: "Pro audio editor", url: "adobe.com/audition", pricing: "Paid", rating: 4.5, tags: ["editing", "adobe", "professional"]},
    {name: "Hindenburg", category: "Audio", subcategory: "Editing", desc: "Podcast editor", url: "hindenburg.com", pricing: "Paid", rating: 4.4, tags: ["editing", "podcast", "voice"]},
    {name: "Alitu", category: "Audio", subcategory: "Podcast", desc: "Podcast maker", url: "alitu.com", pricing: "Paid", rating: 4.2, tags: ["podcast", "easy", "automation"]},
    {name: "Cleanvoice", category: "Audio", subcategory: "Enhancement", desc: "Audio cleanup", url: "cleanvoice.ai", pricing: "Paid", rating: 4.3, tags: ["cleanup", "filler-words", "ai"]},
    {name: "Noise.ai", category: "Audio", subcategory: "Enhancement", desc: "Noise reduction", url: "noise.ai", pricing: "Paid", rating: 4.2, tags: ["noise-reduction", "ai", "real-time"]},
    {name: "Auphonic", category: "Audio", subcategory: "Enhancement", desc: "Audio leveling", url: "auphonic.com", pricing: "Freemium", rating: 4.4, tags: ["leveling", "mastering", "automation"]},
    {name: "Izotope RX", category: "Audio", subcategory: "Repair", desc: "Audio repair", url: "izotope.com/rx", pricing: "Paid", rating: 4.6, tags: ["repair", "professional", "de-noise"]},
    
    // ==================== MUSIC & COMPOSITION ====================
    {name: "AIVA", category: "Audio", subcategory: "Music AI", desc: "AI composer", url: "aiva.ai", pricing: "Freemium", rating: 4.4, tags: ["music", "composition", "ai"], featured: true},
    {name: "Amper Music", category: "Audio", subcategory: "Music AI", desc: "AI music creation", url: "ampermusic.com", pricing: "Paid", rating: 4.1, tags: ["music", "shutterstock", "ai"]},
    {name: "Soundraw", category: "Audio", subcategory: "Music AI", desc: "AI music generator", url: "soundraw.io", pricing: "Paid", rating: 4.3, tags: ["music", "royalty-free", "customizable"]},
    {name: "Ecrett Music", category: "Audio", subcategory: "Music AI", desc: "AI background music", url: "ecrettmusic.com", pricing: "Paid", rating: 4.0, tags: ["music", "background", "ai"]},
    {name: "Beatoven.ai", category: "Audio", subcategory: "Music AI", desc: "AI music for video", url: "beatoven.ai", pricing: "Freemium", rating: 4.1, tags: ["music", "video", "mood"]},
    {name: "Moises.ai", category: "Audio", subcategory: "Stem Separation", desc: "Music separation", url: "moises.ai", pricing: "Freemium", rating: 4.4, tags: ["stems", "separation", "practice"]},
    {name: "Lalal.ai", category: "Audio", subcategory: "Stem Separation", desc: "Voice/music splitter", url: "lalal.ai", pricing: "Freemium", rating: 4.4, tags: ["stems", "vocal-remover", "ai"]},
    {name: "Vocali.se", category: "Audio", subcategory: "Stem Separation", desc: "Vocal remover", url: "vocali.se", pricing: "Freemium", rating: 4.2, tags: ["vocal-remover", "free", "online"]},
    {name: "BandLab", category: "Audio", subcategory: "DAW", desc: "Free online DAW", url: "bandlab.com", pricing: "Free", rating: 4.4, tags: ["daw", "free", "social"]},
    {name: "Soundtrap", category: "Audio", subcategory: "DAW", desc: "Spotify DAW", url: "soundtrap.com", pricing: "Freemium", rating: 4.2, tags: ["daw", "spotify", "collaborative"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE69 = AI_TOOLS_PHASE69;
}


