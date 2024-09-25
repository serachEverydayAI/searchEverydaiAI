function showToast() {
    const toast = document.getElementById("toast");
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 1500); // 1.5초 후에 토스트 메시지를 숨김
}
function submitForm() {
    const keyword1 = document.getElementById('keyword1').innerText;
    const keyword2 = document.getElementById('keyword2').innerText;
    const keyword3 = document.getElementById('keyword3').innerText;
    if (!keyword1 && !keyword2 && !keyword3) {
        showToast();
    } else {
        fetch('/saveCustKeyword/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ keyword1, keyword2, keyword3 }),
        })
        .then(response => {
            if (response.ok) {
                console.log('저장 성공');
                window.location.href = response.url;
            } else {
                return response.json().then(errorData => {
                    showToast(errorData.error);  // 실패 메시지를 toast에 전달
                });
            }
        })
        .catch(error => {
            showToast('서버 오류가 발생했습니다.');  // 네트워크 오류 등 기타 오류 처리
            console.error('Error:', error);
        });
    }
}
