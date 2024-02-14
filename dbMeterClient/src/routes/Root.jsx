import { useState } from 'react'
import reactLogo from '../../src/assets/react.svg'
import viteLogo from '/vite.svg'
import '../style/Style.css'

function App() {
    const [count, setCount] = useState(0)

    return (
        <>
            <h1>ACC DB Meter Application</h1>
            <div className="card">
                <button onClick={() => setCount((count) => count + 1)}>
                    count is {count}
                </button>
                <p>
                    Edit <code>src/routes/Root.jsx</code> and save to test HMR
                </p>
                <p>
                    new routes or children can beadded in the main.jsx file, using the createBrowserRouter method
                </p>
                    <a href="https://reactrouter.com/en/main/routers/create-browser-router">create-browser-router</a>
                <p>
                in general just make new components or routes and put them in the routes or components folders
                </p>
                <a href="https://react.dev/learn/your-first-component">Component Guide</a>
                <p>
                    Routes and components are pretty much the same thing
                </p>
            </div>

        </>
    )
}

export default App
