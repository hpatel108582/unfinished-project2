
import React from 'react';
 
const init = []
 

export function Content() {
    const [list, setList] = React.useState(init);
  const [name, setName] = React.useState('');
 
  function handleChange(event) {
    setName(event.target.value);
  }
 
  function handleAdd() {
    const newList = list.concat({ name });
 
    setList(newList);
  }
 
  return (
    <div>
      <div>
        <input type="text" value={name} onChange={handleChange} />
        <button type="button" onClick={handleAdd}>
          Add
        </button>
      </div>
 
      <ul>
        {list.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}