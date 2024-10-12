function showToast(message) {
    const toast = document.getElementById("toast");
    if (toast) {
        toast.textContent = message;
        toast.classList.add("show");

        setTimeout(() => {
            toast.classList.remove("show");
        }, 1500); // 1.5초 후에 토스트 메시지를 숨김
    } else {
        console.error("Toast element not found!");
    }
}

function keyword_yn() {
    const custId = document.getElementById('cust_id').value;

    $.ajax({
        url: '/keywordyn/',
        type: 'GET',
        data: { cust_id: custId },
        success: function(response) {
            if (response.keyword) {
                console.log(response.keyword);
            } else {
                console.log(response.keyword);
            }
        },
        error: function(xhr) {
            console.error('Error:', xhr);
        }
    });
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
            body: JSON.stringify({ cust_id, keyword1, keyword2, keyword3 }),
        })
        .then(response => {
            if (response.ok) {
                console.log('저장 성공');
                window.location.href = response.url;
            } else {
                return response.json().then(data => {
                    showToast(data.error);  // 실패 메시지를 toast에 전달
                });
            }
        })
        .catch(error => {
            showToast('서버 오류가 발생했습니다.');  // 네트워크 오류 등 기타 오류 처리
            console.error('Error:', error);
        });
    }
}
function move_addSearchWord() {
    const custId = document.getElementById('cust_id').value;

    fetch('/addSearchWordView/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ cust_id: custId }),
    })
    .then(response => {
        if (response.ok) {
            window.location.href = response.url;
        } else {
            return response.json().then(errorData => {
                showToast(errorData.error);  // 실패 메시지를 toast에 전달
            });
        }
    })
}

/* homeTab_Y Script */
function fetchData(url, body) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(body),
    }).then(response => {
        if (!response.ok) throw new Error('Network response was not ok.');
        return response.json();
    });
}

function updateKeywords(data) {
    $('#keyword1').text(data.keyword1);
    $('#keyword2').text(data.keyword2);
    $('#keyword3').text(data.keyword3);
    const formattedDate = data.date.slice(0, 4) + '.' + data.date.slice(4, 6) + '.' + data.date.slice(6, 8);
    $('#date').text(formattedDate + " (" + data.korean_day + ")");
}

function updateNewsContainers(newsData, keywords) {
    const containers = [
        { selector: '#newsContainer1', keyword: keywords.keyword1, summary: '#newsSummary1' },
        { selector: '#newsContainer2', keyword: keywords.keyword2, summary: '#newsSummary2' },
        { selector: '#newsContainer3', keyword: keywords.keyword3, summary: '#newsSummary3' }
    ];

    containers.forEach((container, cnt) => {
        $(container.selector).empty();
        $(container.summary).empty();

        let totalArticleCount = 0;

        const filteredNews = newsData.filter(newsItem =>
            newsItem.keywords && newsItem.keywords.includes(container.keyword)
        );

        const newsCount = filteredNews.length;

        if (newsCount === 0) {
            $(container.selector).append('<div style="margin-top: 20px;">오늘은 관련 뉴스가 없습니다.</div>');
        }

        filteredNews.forEach((newsItem, index) => {
            const isLastItem = index === newsCount - 1;
            const listItem = `
                <div class="list-item" data-link="${newsItem.link}">
                    <div class="news-item" id="newsTitle${index + 1}"><b>${newsItem.title}</b></div>
                    <div class="news-press ellipsis" id="newsPress${index + 1}">${newsItem.press}</div>
                </div>
                <hr class="list-line" style="${isLastItem ? 'margin-bottom: 50px;' : ''}">
            `;

            const articleCount = Number(newsItem.article_cnt);
            totalArticleCount += articleCount;

            $(container.selector).append(listItem);
        });

        if (newsCount > 0) {
            const spanItem = `
                <div class="tab_summary profile" id="newsSummary${cnt + 1}">
                    <img class="bee_img" src="${beeImgSrc}"/>
                    <span>
                        ${totalArticleCount}개 기사를 ${newsCount}개 주제로 정리해드렸어요.
                    </span>
                </div>
            `;
            $(container.summary).append(spanItem);
        }
    });

    // 리스트 항목 클릭 이벤트 추가
    $('.list-item').click(function() {
        const link = $(this).data('link');
        window.open(link, '_blank'); // 새 탭에서 링크 열기
    });
}
