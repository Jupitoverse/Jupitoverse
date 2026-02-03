(function () {
  const API = '/api';
  let llmOptions = [];
  let embeddingOptions = [];
  let chunkingOptions = [];
  let currentProjectId = null;

  const stepsOrder = ['name', 'documents', 'llm', 'embedding', 'chunking', 'build'];

  // --- Tabs ---
  const tabs = document.querySelectorAll('.step-tab');
  const panels = document.querySelectorAll('.step-panel');
  function showStep(step) {
    tabs.forEach((t) => {
      t.classList.toggle('active', t.dataset.step === step);
      t.removeAttribute('aria-disabled');
    });
    panels.forEach((p) => p.classList.toggle('active', p.id === 'panel-' + step));
    if (step === 'chunking') refreshChunkPreview();
    if (step === 'documents') loadDocList();
  }
  tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const step = tab.dataset.step;
      if (step === 'documents' && !currentProjectId) return;
      showStep(step);
    });
  });

  // --- Options APIs ---
  async function loadOptions() {
    try {
      const [llm, emb, chunk] = await Promise.all([
        fetch(API + '/options/llm').then((r) => r.json()),
        fetch(API + '/options/embedding').then((r) => r.json()),
        fetch(API + '/options/chunking').then((r) => r.json()),
      ]);
      llmOptions = llm.options || [];
      embeddingOptions = emb.options || [];
      chunkingOptions = chunk.options || [];
    } catch (e) {
      console.error('Load options failed', e);
    }
  }

  // --- LLM ---
  const llmSelect = document.getElementById('llm-select');
  const llmProsCons = document.getElementById('llm-pros-cons');
  const llmOpenaiKeys = document.getElementById('llm-openai-keys');
  const openaiKeysText = document.getElementById('openai-keys-text');

  function renderLlmProsCons() {
    const id = llmSelect.value;
    const opt = llmOptions.find((o) => o.id === id) || {};
    llmProsCons.innerHTML =
      '<div class="pros">Pros: ' + (opt.pros || '') + '</div><div class="cons">Cons: ' + (opt.cons || '') + '</div>';
    llmOpenaiKeys.style.display = id === 'openai' ? 'block' : 'none';
  }
  llmSelect.addEventListener('change', renderLlmProsCons);

  // --- Embedding ---
  const embeddingSelect = document.getElementById('embedding-select');
  const embeddingProsCons = document.getElementById('embedding-pros-cons');

  function fillEmbeddingSelect() {
    embeddingSelect.innerHTML = embeddingOptions.map((o) => '<option value="' + o.id + '">' + o.name + '</option>').join('');
    renderEmbeddingProsCons();
  }
  function renderEmbeddingProsCons() {
    const id = embeddingSelect.value;
    const opt = embeddingOptions.find((o) => o.id === id) || {};
    embeddingProsCons.innerHTML =
      '<div class="pros">Pros: ' + (opt.pros || '') + '</div><div class="cons">Cons: ' + (opt.cons || '') + '</div>';
  }
  embeddingSelect.addEventListener('change', renderEmbeddingProsCons);

  // --- Chunking ---
  const splitterSelect = document.getElementById('splitter-select');
  const chunkSizeInput = document.getElementById('chunk-size');
  const chunkSizeSlider = document.getElementById('chunk-size-slider');
  const chunkOverlapInput = document.getElementById('chunk-overlap');
  const chunkOverlapSlider = document.getElementById('chunk-overlap-slider');
  const sampleText = document.getElementById('sample-text');
  const chunkingProsCons = document.getElementById('chunking-pros-cons');
  const metricTotalChars = document.getElementById('metric-total-chars');
  const metricNumChunks = document.getElementById('metric-num-chunks');
  const metricAvgChunk = document.getElementById('metric-avg-chunk');
  const chunkPreviewText = document.getElementById('chunk-preview-text');
  const chunkPreviewLabels = document.getElementById('chunk-preview-labels');

  function fillChunkingSelect() {
    splitterSelect.innerHTML = chunkingOptions.map((o) => '<option value="' + o.id + '">' + o.name + '</option>').join('');
    const first = chunkingOptions[0];
    if (first) {
      const minS = first.min_chunk_size != null ? first.min_chunk_size : 20;
      const maxS = first.max_chunk_size != null ? first.max_chunk_size : 2000;
      const maxO = first.max_overlap != null ? first.max_overlap : 500;
      chunkSizeInput.min = minS;
      chunkSizeInput.max = maxS;
      chunkSizeSlider.min = minS;
      chunkSizeSlider.max = Math.min(maxS, 500);
      chunkOverlapInput.min = first.min_overlap != null ? first.min_overlap : 0;
      chunkOverlapInput.max = maxO;
      chunkOverlapSlider.max = Math.min(maxO, 100);
    }
    renderChunkingProsCons();
  }
  splitterSelect.addEventListener('change', () => {
    const opt = chunkingOptions.find((o) => o.id === splitterSelect.value);
    if (opt) {
      chunkSizeInput.min = opt.min_chunk_size;
      chunkSizeInput.max = opt.max_chunk_size;
      chunkSizeSlider.min = opt.min_chunk_size;
      chunkSizeSlider.max = Math.min(opt.max_chunk_size, 500);
      chunkOverlapInput.min = opt.min_overlap;
      chunkOverlapInput.max = opt.max_overlap;
      chunkOverlapSlider.max = Math.min(opt.max_overlap, 100);
      renderChunkingProsCons();
    }
    refreshChunkPreview();
  });

  function renderChunkingProsCons() {
    const id = splitterSelect.value;
    const opt = chunkingOptions.find((o) => o.id === id) || {};
    chunkingProsCons.innerHTML =
      '<div class="pros">Pros: ' + (opt.pros || '') + '</div><div class="cons">Cons: ' + (opt.cons || '') + '</div>';
  }

  chunkSizeInput.addEventListener('input', () => {
    chunkSizeSlider.value = chunkSizeInput.value;
    refreshChunkPreview();
  });
  chunkSizeSlider.addEventListener('input', () => {
    chunkSizeInput.value = chunkSizeSlider.value;
    refreshChunkPreview();
  });
  chunkOverlapInput.addEventListener('input', () => {
    chunkOverlapSlider.value = chunkOverlapInput.value;
    refreshChunkPreview();
  });
  chunkOverlapSlider.addEventListener('input', () => {
    chunkOverlapInput.value = chunkOverlapSlider.value;
    refreshChunkPreview();
  });
  sampleText.addEventListener('input', refreshChunkPreview);

  async function refreshChunkPreview() {
    const text = sampleText.value.trim() || 'This is the text I would like to chunk up. It is the example text for this exercise.';
    const splitter_id = splitterSelect.value || 'character';
    const chunk_size = parseInt(chunkSizeInput.value, 10) || 35;
    const chunk_overlap = parseInt(chunkOverlapInput.value, 10) || 4;
    try {
      const res = await fetch(API + '/chunking/preview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, splitter_id, chunk_size, chunk_overlap }),
      });
      const data = await res.json();
      const metrics = data.metrics || {};
      metricTotalChars.textContent = metrics.total_characters ?? 0;
      metricNumChunks.textContent = metrics.number_of_chunks ?? 0;
      metricAvgChunk.textContent = metrics.average_chunk_size ?? 0;
      const spans = data.spans || [];
      const colors = ['chunk-1', 'chunk-2', 'chunk-3'];
      let html = '';
      const labelItems = [];
      spans.forEach((s) => {
        const escaped = escapeHtml(s.text);
        if (s.type === 'overlap') {
          html += '<span class="span-overlap" title="Overlap">' + escaped + '</span>';
          labelItems.push({ type: 'overlap' });
        } else {
          const idx = (s.chunk_index || 1);
          const cls = colors[(idx - 1) % 3];
          html += '<span class="span-chunk ' + cls + '" title="Chunk #' + idx + '">' + escaped + '</span>';
          labelItems.push({ type: 'chunk', index: idx, cls });
        }
      });
      chunkPreviewText.innerHTML = html || escapeHtml(text);
      chunkPreviewLabels.innerHTML = labelItems.map((item) => {
        if (item.type === 'overlap') return '<span class="label-item"><span class="label-dot" style="background:var(--overlap)"></span> Overlap</span>';
        return '<span class="label-item"><span class="label-dot span-chunk ' + item.cls + '"></span> Chunk #' + item.index + '</span>';
      }).join(' ');
    } catch (e) {
      metricTotalChars.textContent = '-';
      metricNumChunks.textContent = '-';
      metricAvgChunk.textContent = '-';
      chunkPreviewText.textContent = text;
      chunkPreviewLabels.innerHTML = '';
    }
  }
  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // --- Step 1: Create project ---
  const projectNameInput = document.getElementById('project-name');
  const btnCreate = document.getElementById('btn-create-project');
  const createResult = document.getElementById('create-result');
  const nextHint = document.getElementById('next-hint');
  const docNoProject = document.getElementById('doc-no-project');
  const docUploadWrap = document.getElementById('doc-upload-wrap');

  btnCreate.addEventListener('click', async () => {
    const name = (projectNameInput.value || '').trim();
    if (!name) {
      createResult.innerHTML = '<p class="error">Enter a project name.</p>';
      return;
    }
    const project_id = name.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '') || 'project';
    const config = {
      llm: { type: 'ollama_qwen', openai_keys: [] },
      embedding: 'sentence_minilm',
      chunking: { splitter_id: 'character', chunk_size: 512, chunk_overlap: 50 },
    };
    try {
      const res = await fetch(API + '/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ project_id, name, config }),
      });
      const data = await res.json();
      if (res.ok) {
        currentProjectId = project_id;
        createResult.innerHTML = '<p class="success">Project created: ' + name + ' (' + project_id + ').</p>';
        nextHint.style.display = 'block';
        docNoProject.style.display = 'none';
        docUploadWrap.style.display = 'block';
      } else {
        createResult.innerHTML = '<p class="error">' + (typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail || 'Failed')) + '</p>';
      }
    } catch (e) {
      createResult.innerHTML = '<p class="error">Request failed: ' + e.message + '</p>';
    }
  });

  // --- Step 2: Documents (upload store-only, list with file links) ---
  const docDropZone = document.getElementById('doc-drop-zone');
  const docUploadInput = document.getElementById('doc-upload-input');
  const docUploadBrowse = document.getElementById('doc-upload-browse');
  const docFileListEl = document.getElementById('doc-file-list');

  function loadDocList() {
    if (!currentProjectId) {
      docNoProject.style.display = 'block';
      docUploadWrap.style.display = 'none';
      return;
    }
    docNoProject.style.display = 'none';
    docUploadWrap.style.display = 'block';
    fetch(API + '/projects/' + currentProjectId + '/documents/list')
      .then((r) => r.json())
      .then((data) => {
        const files = data.files || [];
        const fileUrl = '/api/projects/' + encodeURIComponent(currentProjectId) + '/documents/file/';
        docFileListEl.innerHTML = files.length === 0
          ? '<li style="color:var(--text-secondary)">No files yet. Drop or browse to upload.</li>'
          : files.map((f) => '<li><span class="file-name">' + escapeHtml(f) + '</span><span class="file-actions"><a href="' + fileUrl + encodeURIComponent(f) + '" target="_blank" rel="noopener">Open</a> <a href="' + fileUrl + encodeURIComponent(f) + '" download>Download</a></span></li>').join('');
      })
      .catch(() => { docFileListEl.innerHTML = '<li style="color:var(--error-color)">Error loading list.</li>'; });
  }

  docUploadBrowse.addEventListener('click', () => docUploadInput.click());
  docDropZone.addEventListener('dragover', (e) => { e.preventDefault(); docDropZone.classList.add('dragover'); });
  docDropZone.addEventListener('dragleave', () => docDropZone.classList.remove('dragover'));
  docDropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    docDropZone.classList.remove('dragover');
    if (!currentProjectId) return;
    const files = e.dataTransfer.files;
    if (files.length) doUpload(Array.from(files));
  });
  docUploadInput.addEventListener('change', function () {
    if (!currentProjectId || !this.files.length) return;
    doUpload(Array.from(this.files));
    this.value = '';
  });

  function doUpload(files) {
    const form = new FormData();
    files.forEach((f) => form.append('files', f));
    fetch(API + '/projects/' + currentProjectId + '/documents/upload?ingest=false', { method: 'POST', body: form })
      .then((r) => r.json())
      .then((data) => {
        loadDocList();
      })
      .catch((e) => { console.error(e); loadDocList(); });
  }

  // --- Save config (when moving to build or when building) ---
  function getConfig() {
    const openaiKeys = [];
    if (llmSelect.value === 'openai' && openaiKeysText.value.trim()) {
      openaiKeysText.value.split('\n').forEach((line) => {
        const i = line.indexOf(':');
        if (i > 0) openaiKeys.push({ tag: line.slice(0, i).trim(), key: line.slice(i + 1).trim() });
      });
    }
    return {
      llm: { type: llmSelect.value, openai_keys: openaiKeys },
      embedding: embeddingSelect.value,
      chunking: {
        splitter_id: splitterSelect.value,
        chunk_size: parseInt(chunkSizeInput.value, 10) || 512,
        chunk_overlap: parseInt(chunkOverlapInput.value, 10) || 50,
      },
    };
  }

  // --- Step 6: Build RAG ---
  const btnBuildRag = document.getElementById('btn-build-rag');
  const buildResult = document.getElementById('build-result');

  btnBuildRag.addEventListener('click', async () => {
    if (!currentProjectId) {
      buildResult.innerHTML = '<p class="error">Create a project in step 1 first.</p>';
      return;
    }
    buildResult.innerHTML = '<p>Updating config and building RAG...</p>';
    try {
      await fetch(API + '/projects/' + currentProjectId, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(getConfig()),
      });
      const ingestRes = await fetch(API + '/projects/' + currentProjectId + '/documents/ingest', { method: 'POST' });
      const ingestData = await ingestRes.json();
      const link = '/project/' + currentProjectId;
      buildResult.innerHTML = '<p class="success">RAG built. Ingested ' + (ingestData.ingested || 0) + ' chunks.</p><p><a href="' + link + '" class="btn btn-primary">Open project</a></p>';
    } catch (e) {
      buildResult.innerHTML = '<p class="error">Build failed: ' + e.message + '</p>';
    }
  });

  // --- Init ---
  loadOptions().then(() => {
    renderLlmProsCons();
    fillEmbeddingSelect();
    fillChunkingSelect();
    refreshChunkPreview();
    if (!currentProjectId) {
      docNoProject.style.display = 'block';
      docUploadWrap.style.display = 'none';
    }
  });
})();
