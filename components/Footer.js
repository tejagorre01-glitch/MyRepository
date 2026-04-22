import styles from './Footer.module.css'

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <p>&copy; 2024 [Your Name]. All rights reserved.</p>
        <p>Built with Next.js</p>
      </div>
    </footer>
  )
}