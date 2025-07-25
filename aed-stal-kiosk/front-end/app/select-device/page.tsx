import Link from "next/link"

export default function Select() {
    return (
        <>
            <Link href="/" className="back">
                Back
            </Link>
            <ul className="device-list">
                <li>
                    <Link href="/device/1">Kut device 1</Link>
                </li>
                <li>
                    <Link href="/device/2">Kut device 2</Link>
                </li>
                <li>
                    <Link href="/device/3">Kut device 3</Link>
                </li>
                <li>
                    <Link href="/device/4">Kut device 4</Link>
                </li>
                <li>
                    <Link href="/device/5">Kut device 5</Link>
                </li>
                <li>
                    <Link href="/device/6">Kut device 6</Link>
                </li>
            </ul>
        </>
    )
}
