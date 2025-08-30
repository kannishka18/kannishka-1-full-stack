document.addEventListener('click', async (e)=>{
  const likeBtn = e.target.closest('.like-btn');
  if(likeBtn){
    const url = likeBtn.dataset.url;
    const res = await fetch(url, {method:'POST', headers:{'X-CSRFToken': csrftoken}});
    if(res.ok){
      const data = await res.json();
      likeBtn.querySelector('.like-count').textContent = data.count;
      likeBtn.classList.toggle('btn-outline-primary', !data.liked);
      likeBtn.classList.toggle('btn-primary', data.liked);
    }
  }
  const followBtn = e.target.closest('.follow-btn');
  if(followBtn){
    const url = followBtn.dataset.url;
    const res = await fetch(url, {method:'POST', headers:{'X-CSRFToken': csrftoken}});
    if(res.ok){
      const data = await res.json();
      followBtn.textContent = data.following ? 'Unfollow' : 'Follow';
    }
  }
});
