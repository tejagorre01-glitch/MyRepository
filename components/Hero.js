import styles from './Hero.module.css'

export default function Hero() {
  return (
    <section className={styles.hero} id="about">
      <div className={styles.container}>
        <h1 className={styles.title}> Hi, I'm Teja </h1>
        <p className={styles.subtitle}>Full Stack Developer | Designer | Problem Solver</p>
        <p className={styles.description}>
          I have knowledge on Python, Artificial Intelligence and AWS Cloud, and I am passionate about building 
          real-world applications. 
          I have worked on projects like Designing High Availability Architecture on AWS, Crop Yield Prediction, 
          and an Expense Tracker. I aim to grow my skills in Cybersecurity with AI while starting 
          my career in the AI and IT industries.

        </p>
        <a href="#projects" className={styles.cta}>View My Work</a>
      </div>
    </section>
  )
}