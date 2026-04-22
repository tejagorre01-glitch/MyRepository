import styles from './Skills.module.css'

const skills = [
  {
    name: 'Python',
    description: 'A high-level programming language known for its simplicity and versatility.'
  },
  {
    name: 'CSS',
    description: 'A stylesheet language used for describing the presentation of web pages.'
  },
  {
    name: 'HTML',
    description: 'The standard markup language for creating web pages and web applications.'
  },
  {
    name: 'Cloud Computing',
    description: 'On-demand delivery of IT resources -such as servers, storage, databases, and software -over the internet with pay-as-you-go pricing'
  }
]

export default function Skills() {
  return (
    <section className={styles.skills} id="skills">
      <div className={styles.container}>
        <h2 className={styles.title}>Skills & Technologies</h2>
        <div className={styles.grid}>
          {skills.map((skill, index) => (
            <div key={index} className={styles.skill}>
              <div className={styles.skillName}>{skill.name}</div>
              <div className={styles.skillDescription}>{skill.description}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}