import Link from "next/link"

export default function Select() {
    return (
        <>
            <Link href="/" className="back">
                Back
            </Link>
            <ul className="device-list">
                <li>Kut device 1</li>
                <li>Kut device 2</li>
                <li>Kut device 3</li>
                <li>Kut device 4</li>
                <li>Kut device 5</li>
                <li>Kut device 6</li>
            </ul>
        </>
    )
}
