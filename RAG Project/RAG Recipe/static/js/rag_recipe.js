(function () {
  const listEl = document.getElementById('project-list');
  if (!listEl) return;
  fetch('/api/projects')
    .then((r) => r.json())
    .then((data) => {
      const projects = (data && data.projects) || [];
      if (projects.length === 0) {
        listEl.innerHTML = '<p>No projects yet. Use <a href="/add-project" target="_blank">Add Project</a> to create one.</p>';
        return;
      }
      listEl.innerHTML =
        '<ul class="project-list-ul">' +
        projects
          .map(
            (p) =>
              '<li><a href="/project/' +
              p.project_id +
              '"><strong>' +
              (p.name || p.project_id) +
              '</strong></a> <code>' +
              p.project_id +
              '</code>' +
              (p.archived ? ' <span class="archived">archived</span>' : '') +
              '</li>'
          )
          .join('') +
        '</ul>';
    })
    .catch(() => {
      listEl.innerHTML = '<p>Could not load projects.</p>';
    });
})();
