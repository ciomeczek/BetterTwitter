const PostElement = ({ items })=> (
    <ul>
        {items.map(({ title, text, key })=><li key={key}>{title} {text}</li>)}
    </ul>
)
export default PostElement;