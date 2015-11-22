class ArticleItem extends React.Component
{
  render()
  {
    var article = this.props.article;
    var site = this.props.article.site;
    return(
      <div>
        <h4 className="list-group-item-heading">
          <a href={article.url}>{article.title}</a>&nbsp;
          <small>from&nbsp;<a href={site.url}>{site.title}</a></small>
        </h4>
        <p className="list-group-item-text" style={{marginLeft: '1em'}}>{article.description}</p>
        <p className="text-right">{article.published_date}</p>
      </div>
    );    
  }  
}

class App extends React.Component
{
  constructor(props) {
    super(props);
    this.state = {
      articles: []
    };
    this.fetchLatestArticles();
  }

  fetchLatestArticles() {
    $.ajax({
      url: "../dmy/articles.json",
      dataType: 'json',
      cache: false,
      success: (data) => {
        this.setState({articles: data.articles});
      },
      error: (xhr, status, err) => {
        console.error("", status, err.toString());
      }
    });
  }

  render() {
    var articleItems = this.state.articles.map((article) => {
      return (
        <li className="list-group-item">
          <ArticleItem article={article} />
        </li>
      );
    });
    return(
      <ul className="list-group">
        {articleItems}
      </ul>
    );
  }
}


ReactDOM.render(
  <App />,
  document.getElementById('main')
);
