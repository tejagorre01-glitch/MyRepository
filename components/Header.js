import styles from './Header.module.css'
import ThemeToggle from './ThemeToggle'

export default function Header() {
  return (
    <header className={styles.header}>
      <nav className={styles.nav}>
        <div className={styles.logo}>
          <h1>My Portfolio</h1>
        </div>
        <div className={styles.navRight}>
          <ThemeToggle />
          <ul className={styles.navList}>
            <li><a href="#about">About</a></li>
            <li><a href="#projects">Projects</a></li>
            <li><a href="#skills">Skills</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </div>
      </nav>
    </header>
  )
}